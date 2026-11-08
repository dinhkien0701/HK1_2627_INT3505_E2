from flask import Blueprint, jsonify
from sqlalchemy import text
from ..extensions import db

# Tạo Blueprint riêng cho Health, không có prefix (để URL là /healthz luôn)
health_bp = Blueprint("health", __name__, url_prefix="")

# 1. LIVENESS PROBE: Chỉ kiểm tra xem Process (tiến trình) còn sống không.
# Không được gọi Database ở đây để tránh bị restart nhầm.
@health_bp.get("/healthz")
def liveness():
    return jsonify({"status": "ok"}), 200

# 2. READINESS PROBE: Kiểm tra xem hệ thống đã sẵn sàng nhận traffic chưa.
# Bắt buộc phải check kết nối Database (hoặc Cache).
@health_bp.get("/ready")
def readiness():
    checks = {}
    
    # Thử chạy một câu lệnh SQL đơn giản để test kết nối
    try:
        db.session.execute(text("SELECT 1"))
        checks["db"] = "ok"
    except Exception:
        checks["db"] = "err"

    # Nếu tất cả các check đều "ok" thì trả 200, ngược lại trả 503
    is_ready = all(v == "ok" for v in checks.values())
    
    return jsonify({
        "status": "ok" if is_ready else "degraded",
        "checks": checks
    }), 200 if is_ready else 503