
# Bài tập tuần 7: Backend Service - Product & Order API

Dự án Backend Service xây dựng bằng Flask, hoàn thiện chuỗi bài tập từ Lab 1 đến Lab 5. Hệ thống áp dụng kiến trúc Application Factory, Blueprint, ORM và được đóng gói chuẩn Production.

### Công nghệ sử dụng
*   **Core:** Python, Flask
*   **Database/ORM:** SQLAlchemy 2.x, Flask-Migrate (Alembic), PostgreSQL / SQLite
*   **Validation:** Marshmallow
*   **Testing:** Pytest
*   **Deployment:** Docker, Gunicorn

---

### Tóm tắt các bài tập đã hoàn thiện

*   **Bài 1 - Product CRUD:** Xây dựng cấu trúc dự án chuẩn (Application Factory, Blueprint). Viết API CRUD cho `Product`, tích hợp validate dữ liệu qua Marshmallow và xử lý lỗi tập trung (400, 404, 409, 422).
*   **Bài 2 - Order Resource:** Bổ sung bảng `Order` và `OrderItem` (Quan hệ 1-N). Tạo Blueprint riêng `/api/v1/orders`. Xử lý logic đặt hàng: kiểm tra tồn kho và tự động trừ số lượng sản phẩm.
*   **Bài 3 - Dockerize:** Đóng gói toàn bộ service bằng `Dockerfile` (multi-stage) và `docker-compose.yml`. Hệ thống tự động chạy Migration và kết nối với PostgreSQL khi khởi động.
*   **Bài 4 - Health Checks:** Tách biệt 2 endpoint kiểm tra sức khỏe:
    *   `/healthz` (Liveness): Kiểm tra process còn sống.
    *   `/ready` (Readiness): Kiểm tra kết nối Database trước khi nhận traffic.
*   **Bài 5 - Unit Test:** Viết Pytest cho API POST và GET. Áp dụng `selectinload` (eager loading) cho quan hệ 1-N và viết hàm đếm số truy vấn SQL để chứng minh hệ thống không bị lỗi N+1.

---

### Hướng dẫn khởi chạy

**1. Chạy trực tiếp (Local)**
```bash
# Cài đặt thư viện
pip install -r requirements.txt

# Set biến môi trường (Linux/Mac)
export PYTHONPATH=src

# Chạy server
flask --app wsgi db upgrade
flask --app wsgi run --debug
```

**2. Chạy bằng Docker (Khuyên dùng)**
```bash
docker compose up --build
```
*(API sẽ hoạt động tại `http://127.0.0.1:5000`)*

**3. Chạy Unit Test**
```bash
export PYTHONPATH=src
pytest tests/ -v -s
```