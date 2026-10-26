# Nộp bài tập về nhà tuần 6 - SOA

## Giới thiệu
Repository này chứa bài giải cho bài tập về nhà Buổi 06: **Authentication và Authorization**. 
Bài làm tập trung vào việc thiết kế API Social Network và phân tích các rủi ro bảo mật liên quan đến xác thực và phân quyền.

## Cấu trúc bài nộp
- **`openapi.yaml`**: Đặc tả OpenAPI 3.0 cho 3 endpoint:
  - `POST /auth/login`
  - `POST /auth/refresh`
  - `GET /posts/{id}`
  - *Đã trả lời rõ ràng trong spec:* Scope yêu cầu, các lỗi có thể xảy ra, và Status Code tương ứng.
- **`SecurityAudit.md`**: Báo cáo kiểm toán bảo mật, liệt kê chi tiết **6 điểm lỗ hổng tiềm ẩn** (vượt yêu cầu tối thiểu 5 điểm). Các lỗ hổng được ánh xạ theo tiêu chuẩn OWASP API Security Top 10 và các rủi ro JWT đã học trong bài giảng (BOLA, XSS token, thiếu Revocation, alg=none, PII trong JWT, Brute-force).

## Cách xem
- Mở file `openapi.yaml` bằng **Swagger Editor** (https://editor.swagger.io/) để xem giao diện trực quan của API.
- Đọc file `SecurityAudit.md` để xem chi tiết các kịch bản tấn công và biện pháp khắc phục.
