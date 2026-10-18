from flask import Blueprint, request, jsonify
from models import db, Book, Category
from sqlalchemy import or_, and_
import base64
import json

books_bp = Blueprint('books', __name__, url_prefix='/api/v1')

# --- CÁC HÀM HELPER CHO CURSOR (Theo slide trang 24) ---
def _enc(s): 
    """Mã hóa dict thành Base64 (bỏ dấu = ở cuối cho URL sạch)"""
    return base64.urlsafe_b64encode(json.dumps(s).encode()).decode().rstrip("=")

def _dec(t):
    """Giải mã Base64 thành dict"""
    pad = "=" * (-len(t) % 4)
    return json.loads(base64.urlsafe_b64decode(t + pad).decode())

# --- HÀM PARSE SORT MULTI-KEY (Mở rộng từ slide trang 23) ---
def parse_sort(raw_sort):
    # Whitelist các cột được phép sort (chống SQL Injection)
    ALLOWED_SORTS = {
        "id": Book.id,
        "price_vnd": Book.price_vnd,
        "title": Book.title
    }
    
    cols = []
    sort_meta = [] # Lưu lại info để build cursor
    
    for s in raw_sort.split(','):
        s = s.strip()
        if not s: continue
        
        desc = s.startswith("-")
        key = s.lstrip("-")
        
        if key not in ALLOWED_SORTS:
            return None, None, f"Sort key '{key}' không hợp lệ"
            
        col = ALLOWED_SORTS[key]
        cols.append(col.desc() if desc else col.asc())
        sort_meta.append({"key": key, "desc": desc})
        
    # Luôn thêm id làm tie-breaker (như slide trang 23 giải thích)
    if not any(m["key"] == "id" for m in sort_meta):
        cols.append(Book.id.desc() if sort_meta[0]["desc"] else Book.id.asc())
        sort_meta.append({"key": "id", "desc": sort_meta[0]["desc"]})
        
    return cols, sort_meta, None

# --- HÀM APPLY CURSOR (Cốt lõi của Composite Key - slide trang 24) ---
def apply_cursor(query, raw_cursor, sort_meta):
    if not raw_cursor:
        return query, None
        
    try:
        c = _dec(raw_cursor)
        # Kiểm tra xem cursor có khớp với sort hiện tại không
        current_sort_str = request.args.get('sort', '-id')
        if c.get("sort_str") != current_sort_str:
            return None, "Sort condition changed. Invalid cursor."
            
        vals = c["vals"]
        
        # Xây dựng điều kiện WHERE phức tạp (Tương đương tuple_ < tuple_ trong SQL)
        # VD sort: -price, id => WHERE price < v1 OR (price = v1 AND id > v2)
        conditions = []
        for i in range(len(sort_meta)):
            sub_conds = []
            
            # Các điều kiện trước đó phải BẰNG
            for j in range(i):
                col_j = getattr(Book, sort_meta[j]["key"])
                sub_conds.append(col_j == vals[j])
                
            # Điều kiện hiện tại phải LỚN HƠN hoặc NHỎ HƠN
            col_i = getattr(Book, sort_meta[i]["key"])
            val_i = vals[i]
            
            if sort_meta[i]["desc"]:
                sub_conds.append(col_i < val_i)
            else:
                sub_conds.append(col_i > val_i)
                
            conditions.append(and_(*sub_conds))
            
        return query.filter(or_(*conditions)), None
    except Exception:
        return None, "Invalid cursor format"

# --- MAIN ROUTE ---
@books_bp.route('/books', methods=['GET'])
def list_books():
    strategy = request.args.get('strategy', 'offset') # Mặc định offset
    limit = min(request.args.get('limit', 20, type=int), 100) # Default 20, Max 100
    
    # 1. Base Query
    query = Book.query
    
    # 2. Filter ?genre (Dựa vào bảng Entities, genre map với Category.slug)
    genre = request.args.get('genre')
    if genre:
        query = query.join(Category).filter(Category.slug == genre)
        
    # 3. Sort Multi-key
    sort_str = request.args.get('sort', '-id')
    cols, sort_meta, sort_err = parse_sort(sort_str)
    if sort_err:
        return jsonify({"error": sort_err}), 400
    query = query.order_by(*cols)

    # 4. Pagination Strategy
    if strategy == 'offset':
        page = request.args.get('page', 1, type=int)
        offset = (page - 1) * limit
        
        # Đếm tổng số (tuỳ chọn, hữu ích cho Offset)
        total = query.count()
        books = query.offset(offset).limit(limit).all()
        
        return jsonify({
            "data": [b.to_dict() for b in books],
            "pagination": {
                "strategy": "offset",
                "page": page,
                "limit": limit,
                "total": total,
                "has_next": offset + len(books) < total
            }
        }), 200

    elif strategy == 'cursor':
        raw_cursor = request.args.get('cursor')
        
        # Áp dụng cursor vào query
        query, cursor_err = apply_cursor(query, raw_cursor, sort_meta)
        if cursor_err:
            return jsonify({"error": cursor_err}), 400
            
        # Lấy limit + 1 để check xem còn data không (Slide trang 21)
        books = query.limit(limit + 1).all()
        has_more = len(books) > limit
        books = books[:limit]
        
        # Tạo next_cursor (Slide trang 24)
        next_cursor = None
        if books and has_more:
            last_book = books[-1]
            vals = [getattr(last_book, m["key"]) for m in sort_meta]
            next_cursor = _enc({"sort_str": sort_str, "vals": vals})
            
        return jsonify({
            "data": [b.to_dict() for b in books],
            "pagination": {
                "strategy": "cursor",
                "limit": limit,
                "next_cursor": next_cursor,
                "has_more": has_more
            }
        }), 200
        
    else:
        return jsonify({"error": "Strategy không hợp lệ. Chỉ dùng 'offset' hoặc 'cursor'."}), 400