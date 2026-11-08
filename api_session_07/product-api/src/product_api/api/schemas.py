# bài tập 1 #

from marshmallow import Schema, fields, validate

# 1. Dùng để trả dữ liệu ra cho Client (Output)
class ProductOut(Schema):
    id = fields.Int()
    sku = fields.String()
    name = fields.String()
    description = fields.String(allow_none=True)
    price_cents = fields.Int()
    qty_in_stock = fields.Int()
    archived = fields.Bool()

# 2. Dùng để nhận dữ liệu tạo mới (Input)
class ProductIn(Schema):
    sku = fields.String(required=True, validate=validate.Length(min=3, max=32))
    name = fields.String(required=True, validate=validate.Length(min=1, max=255))
    description = fields.String(allow_none=True)
    price_cents = fields.Int(required=True, validate=validate.Range(min=0))
    qty_in_stock = fields.Int(load_default=0, validate=validate.Range(min=0))

# 3. Dùng để cập nhật một phần (PATCH)
class ProductPatch(Schema):
    name = fields.String(validate=validate.Length(min=1, max=255))
    price_cents = fields.Int(validate=validate.Range(min=0))
    description = fields.String(allow_none=True)

# 4. Dùng cho endpoint Reserve (Đặt hàng)
class ReserveIn(Schema):
    qty = fields.Int(required=True, validate=validate.Range(min=1))



# Bài tập 2 #

# --- SCHEMAS CHO ORDER ---
class OrderItemIn(Schema):
    product_id = fields.Int(required=True)
    quantity = fields.Int(required=True, validate=validate.Range(min=1))

class OrderIn(Schema):
    items = fields.List(fields.Nested(OrderItemIn), required=True)

class OrderItemOut(Schema):
    product_id = fields.Int()
    quantity = fields.Int()

class OrderOut(Schema):
    id = fields.Int()
    created_at = fields.DateTime()
    items = fields.List(fields.Nested(OrderItemOut))