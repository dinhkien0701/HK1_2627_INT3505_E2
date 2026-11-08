# bài tập 2#

from flask import Blueprint, jsonify, request
from marshmallow import ValidationError
from ..extensions import db
from ..models.order import Order, OrderItem
from ..models.product import Product
from .schemas import OrderIn, OrderOut
from .errors import NotFound, OutOfStock

orders_bp = Blueprint("orders", __name__, url_prefix="/api/v1/orders")

# API: Tạo đơn hàng mới (POST /api/v1/orders)
@orders_bp.post("")
def create_order():
    try:
        body = OrderIn().load(request.json)
    except ValidationError as err:
        return jsonify({"code": "validation_error", "message": err.messages}), 422

    order = Order()
    db.session.add(order)
    
    # Duyệt qua từng sản phẩm khách muốn mua
    for item_data in body["items"]:
        product = db.session.get(Product, item_data["product_id"])
        
        if not product or product.archived:
            raise NotFound(message=f"Product ID {item_data['product_id']} not found")
        
        if product.qty_in_stock < item_data["quantity"]:
            raise OutOfStock(message=f"Product {product.sku} only has {product.qty_in_stock} left")

        # Trừ tồn kho
        product.qty_in_stock -= item_data["quantity"]
        
        # Thêm vào bảng OrderItem
        order_item = OrderItem(
            product_id=product.id,
            quantity=item_data["quantity"]
        )
        order.items.append(order_item)

    db.session.commit()
    return OrderOut().dump(order), 201