# bài tập 1#

#blueprint products_bp: Tạo 1 nhóm các route liên quan đến sản phẩm, có thể gộp chung prefix /api/v1/products
#blue print là tính năng trong thư viện flask
#blueprint dùng để chia nhỏ thành các nhóm trong nội bộ để dễ thao tác

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from ..extensions import db
from ..models.product import Product
from .schemas import ProductOut, ProductIn, ProductPatch, ReserveIn
from .errors import Conflict, OutOfStock, NotFound

products_bp = Blueprint("products", __name__, url_prefix="/api/v1/products")

# 1. GET /api/v1/products (Lấy danh sách + Phân trang)
@products_bp.get("")
def list_products():
    page = max(1, int(request.args.get("page", 1)))
    size = min(100, max(1, int(request.args.get("size", 20))))

    # Chỉ lấy sản phẩm chưa bị xóa mềm (archived=False)
    base_query = db.select(Product).where(Product.archived.is_(False))
    
    # Đếm tổng số lượng
    total = db.session.scalar(
        db.select(db.func.count()).select_from(Product).where(Product.archived.is_(False))
    )

    # Phân trang
    rows = db.session.execute(
        base_query.order_by(Product.id).offset((page - 1) * size).limit(size)
    ).scalars().all()

    return jsonify({
        "items": [ProductOut().dump(p) for p in rows],
        "page": page,
        "size": size,
        "total": total
    }), 200


# Lấy sản phẩm theo id
@products_bp.get("/<int:id>")
def get_product(id):
    p = db.get_or_404(Product, id)
    if p.archived:
        raise NotFound(message="Product not found or deleted")
    return ProductOut().dump(p), 200


# (Tạo sản phẩm mới)
@products_bp.post("")
def create_product():
    try:
        body = ProductIn().load(request.json)
    except ValidationError as err:
        return jsonify({"code": "validation_error", "message": err.messages}), 422

    p = Product(**body)
    db.session.add(p)
    
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback() # Quan trọng: Phải rollback nếu lỗi DB
        raise Conflict(message="SKU already exists")

    return ProductOut().dump(p), 201


# post : gửi thông tin đặt trước
@products_bp.post("/<int:id>/reserve")
def reserve_product(id):
    try:
        body = ReserveIn().load(request.json)
    except ValidationError as err:
        return jsonify({"code": "validation_error", "message": err.messages}), 422

    p = db.get_or_404(Product, id)
    qty = body["qty"]

    if p.archived:
        raise NotFound(message="Product not found or deleted")

    if p.qty_in_stock < qty:
        raise OutOfStock(message=f"Only {p.qty_in_stock} left")

    p.qty_in_stock -= qty
    db.session.commit()
    return ProductOut().dump(p), 200


# 5. PATCH /api/v1/products/<int:id> (Cập nhật một phần)
@products_bp.patch("/<int:id>")
def patch_product(id):
    p = db.get_or_404(Product, id)
    if p.archived:
        raise NotFound(message="Product not found or deleted")

    try:
        # partial=True cho phép client chỉ gửi 1 vài field cần sửa
        body = ProductPatch().load(request.json, partial=True)
    except ValidationError as err:
        return jsonify({"code": "validation_error", "message": err.messages}), 422

    for k, v in body.items():
        setattr(p, k, v)
    
    db.session.commit()
    return ProductOut().dump(p), 200


# 6. DELETE /api/v1/products/<int:id> (Xóa mềm)
@products_bp.delete("/<int:id>")
def delete_product(id):
    p = db.get_or_404(Product, id)
    p.archived = True # Xóa mềm: Chỉ đánh dấu archived=True
    db.session.commit()
    return "", 204