from flask import Flask, jsonify, request
import base64, json, uuid
from datetime import datetime, timedelta

app = Flask(__name__)

# 1. Tạo Mock Data (25 đơn hàng)
orders_db = []
statuses = ["paid", "pending", "shipped"]
for i in range(1, 26):
    orders_db.append({
        "id": str(uuid.uuid4()),
        "customer_id": f"cust_{i % 5 + 1}",
        "status": statuses[i % 3],
        "total": round(10.5 * i, 2),
        "created_at": (datetime(2026, 1, 1) + timedelta(days=i)).isoformat()
    })
# Sắp xếp mặc định ban đầu để đảm bảo tính ổn định
orders_db.sort(key=lambda x: (x["created_at"], x["id"]), reverse=True)

# 2. Helper functions cho Cursor (Base64 Encode/Decode)
def encode_cursor(item, sort_key):
    payload = {"sort_val": item[sort_key], "id": item["id"]}
    return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()

def decode_cursor(cursor_str):
    try:
        decoded = base64.urlsafe_b64decode(cursor_str.encode()).decode()
        return json.loads(decoded)
    except Exception:
        return None

# 3. Endpoint GET /orders
@app.route('/orders', methods=['GET'])
def get_orders():
    # Lấy tham số
    limit = max(1, min(int(request.args.get('limit', 10)), 100))
    fields_param = request.args.get('fields')
    status_filter = request.args.get('status')
    customer_filter = request.args.get('customer_id')
    sort_param = request.args.get('sort', '-created_at') # Mặc định mới nhất
    cursor_str = request.args.get('cursor')

    # Validate Sparse Fieldsets
    allowed_fields = {"id", "customer_id", "status", "total", "created_at"}
    if fields_param:
        requested_fields = {f.strip() for f in fields_param.split(',')}
        if not requested_fields.issubset(allowed_fields):
            return jsonify({"error": "Invalid fields parameter"}), 400

    # Filtering
    data = orders_db[:]
    if status_filter:
        data = [o for o in data if o["status"] == status_filter]
    if customer_filter:
        data = [o for o in data if o["customer_id"] == customer_filter]

    # Sorting (Xử lý dấu '-' cho descending)
    reverse = sort_param.startswith('-')
    sort_key = sort_param.lstrip('-')
    if sort_key not in allowed_fields:
        return jsonify({"error": "Invalid sort field"}), 400
    
    # Luôn thêm 'id' làm tie-breaker để cursor hoạt động chính xác
    data.sort(key=lambda x: (x[sort_key], x["id"]), reverse=reverse)

    # Cursor Logic
    if cursor_str:
        cursor_data = decode_cursor(cursor_str)
        if not cursor_data:
            return jsonify({"error": "Invalid cursor"}), 400
        
        last_val = cursor_data["sort_val"]
        last_id = cursor_data["id"]
        
        # Lọc các item nằm sau cursor dựa trên sort order
        filtered = []
        for item in data:
            item_val = item[sort_key]
            item_id = item["id"]
            if reverse:
                if (item_val < last_val) or (item_val == last_val and item_id < last_id):
                    filtered.append(item)
            else:
                if (item_val > last_val) or (item_val == last_val and item_id > last_id):
                    filtered.append(item)
        data = filtered

    # Phân trang
    paginated_items = data[:limit]
    
    # Tạo next_cursor nếu còn dữ liệu
    next_cursor = None
    if len(paginated_items) == limit and len(data) > limit:
        next_cursor = encode_cursor(paginated_items[-1], sort_key)

    # Áp dụng Sparse Fieldsets
    if fields_param:
        requested_fields = [f.strip() for f in fields_param.split(',')]
        result_data = [{k: v for k, v in item.items() if k in requested_fields} for item in paginated_items]
    else:
        result_data = paginated_items

    return jsonify({
        "data": result_data,
        "next_cursor": next_cursor
    })

if __name__ == "__main__":
    app.run(host = "127.0.0.1", port = 5000 , debug = True)

