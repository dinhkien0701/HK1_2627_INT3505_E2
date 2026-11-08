import pytest
from product_api.factory import create_app
from product_api.config import DefaultConfig
from product_api.extensions import db
from product_api.models.product import Product

@pytest.fixture
def app():
    app = create_app(DefaultConfig)
    # Cấu hình lại DB dùng RAM (in-memory) để test cho nhanh và không bẩn DB thật
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    
    with app.app_context():
        db.create_all()
        # Tạo sẵn 1 sản phẩm mẫu (id=1) để test các endpoint GET/Order
        p = Product(sku="TEST01", name="SP Test", price_cents=1000, qty_in_stock=10)
        db.session.add(p)
        db.session.commit()
        
        yield app # Trả app ra cho các hàm test dùng
        
        db.session.remove()
        db.drop_all() # Xóa sạch DB sau khi test xong

@pytest.fixture
def client(app):
    return app.test_client()