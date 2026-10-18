# Bài tập tuần 5

Dự án xây dựng RESTful API cơ bản cho hệ thống Bookstore, được thực hiện trong khuôn khổ Lab 1 môn học. Dự án tập trung vào việc thiết kế Data Model, Resource Design và triển khai các cơ chế phân trang nâng cao.

## Tính năng chính
- **CRUD cơ bản:** Lấy danh sách sách (`GET`).
- **Filtering:** Lọc sách theo thể loại (`?genre=...`).
- **Sorting:** Hỗ trợ sắp xếp đa tiêu chí (multi-key sort), ví dụ: `?sort=-price_vnd,title`.
- **Pagination:** Hỗ trợ 2 chiến lược phân trang (chọn qua `?strategy=...`):
  - `offset`: Phân trang truyền thống (dùng `page`, `limit`).
  - `cursor`: Phân trang bằng con trỏ (Composite Cursor kết hợp Base64) giúp tối ưu hiệu năng và tránh trùng lặp dữ liệu.

## 🛠 Công nghệ sử dụng
- **Ngôn ngữ:** Python 3.11+
- **Framework:** Flask
- **ORM:** Flask-SQLAlchemy
- **Cơ sở dữ liệu:** SQLite
- **Công cụ test:** Postman

##  Cấu trúc thư mục
```text
bookstore-api/
├── app.py                  # File khởi chạy ứng dụng và seed data
├── models.py               # Định nghĩa các Entities (Book, Category)
├── routes/
│   └── books.py            # Chứa logic API (Filter, Sort, Pagination)
├── schemas/
│   └── book.json           # JSON Schema dùng để validate dữ liệu (cho các lab sau)
├── api session 5.postman_collection.json  # Bộ test API (dùng cho Postman)
└── README.md               # Tài liệu hướng dẫn dự án