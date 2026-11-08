# bài 1 #
from flask import Flask, jsonify
from .extensions import db, migrate
from .config import DefaultConfig
from .api.products import products_bp
from .api.orders import orders_bp
from .api.health import health_bp
from .api.errors import ApiError 

def create_app(config_class=DefaultConfig):
    # bọc app=flask vào hàm để có thể tạo nhiều app với các config khác nhau
    # bọc để tránh gọi db.init_app(app) trước khi app được tạo ra, vì db.init_app(app) cần app đã được tạo ra
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    db.init_app(app)
    migrate.init_app(app, db)
    
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(health_bp)

    # bắt lỗi tự động
    @app.errorhandler(ApiError)
    def handle_api_error(error):
        response = jsonify({
            "code": error.code,
            "message": error.message
        })
        response.status_code = error.status_code
        return response
    #

    return app