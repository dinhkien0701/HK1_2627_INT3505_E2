# Security Audit Report - Social Network API

Dựa trên các kiến thức về Authentication & Authorization (Buổi 06) và tiêu chuẩn OWASP API Security Top 10, dưới đây là **6 điểm lỗ hổng/rủi ro bảo mật** có thể xảy ra trong thiết kế API hiện tại.

### 1. Lỗi BOLA (Broken Object Level Authorization) - Rủi ro: CRITICAL
- **Mô tả:** Endpoint `GET /posts/{id}` chỉ kiểm tra xem user đã có scope `posts:read` hay chưa, mà thiếu bước kiểm tra quyền sở hữu đối với tài nguyên (Ownership). 
- **Kịch bản lộ:** User A đăng nhập hợp lệ, dùng ID `post_99` (bài viết ở chế độ Private của User B) để gọi API. Hệ thống vẫn trả về dữ liệu vì không check `post.author_id == current_user.id`.
- **Khắc phục:** Áp dụng thêm lớp kiểm tra quyền đối tượng (ví dụ dùng decorator `@user_owns_resource`).

### 2. JWT bị đánh cắp do lưu trữ không an toàn - Rủi ro: HIGH
- **Mô tả:** Nếu Frontend lưu trữ `access_token` và `refresh_token` trong `localStorage` hoặc `sessionStorage`, token có thể bị đánh cắp nếu xảy ra lỗ hổng XSS.
- **Kịch bản lộ:** Kẻ tấn công chèn mã JavaScript độc hại vào nội dung một bài post. Khi user khác xem bài viết, script tự động chạy và gửi `localStorage.getItem('token')` về server của hacker.
- **Khắc phục:** Sử dụng mô hình BFF (Backend for Frontend) hoặc lưu token vào Cookie với các cờ `HttpOnly`, `Secure`, `SameSite`.

### 3. Token không thể thu hồi ngay lập tức (Revocation) - Rủi ro: HIGH
- **Mô tả:** JWT mang bản chất stateless. Nếu `access_token` bị lộ hoặc user đã Logout, token vẫn còn hiệu lực đến khi hết hạn (15 phút). 
- **Kịch bản lộ:** Nhân viên bị sa thải đã kịp lấy `refresh_token`. Nếu API `/auth/refresh` không kiểm tra blocklist (Redis), nhân viên này vẫn có thể duy trì quyền truy cập vô thời hạn.
- **Khắc phục:** Cài đặt cơ chế blocklist lưu `jti` (JWT ID) vào Redis khi logout. Đặt thời gian sống (exp) của Access Token thật ngắn.

### 4. Algorithm Confusion / alg=none - Rủi ro: CRITICAL
- **Mô tả:** Lỗi cấu hình thư viện JWT (như Flask-JWT-Extended) khiến server chấp nhận thuật toán do client tự khai báo trong Header.
- **Kịch bản lộ:** Kẻ tấn công tạo một token giả có header `{"alg": "none"}` (không cần chữ ký) hoặc đổi từ `RS256` sang `HS256`, sau đó gửi request. Nếu server không whitelist thuật toán, nó sẽ chấp nhận token giả mạo này.
- **Khắc phục:** Cấu hình cứng thuật toán (ví dụ `JWT_ALGORITHM="HS256"`) và từ chối mọi token có header `alg` không nằm trong allowlist.

### 5. Rò rỉ dữ liệu nhạy cảm (PII) qua JWT Payload - Rủi ro: MEDIUM
- **Mô tả:** Payload của JWT chỉ được mã hóa Base64 (ai cũng decode được). 
- **Kịch bản lộ:** Lập trình viên tiện tay nhét các thông tin như số điện thoại, email, hoặc tệ hơn là mật khẩu/mã PIN vào phần claims của token. Kẻ tấn công chỉ cần chặn được token hoặc xem log là có thể đọc được toàn bộ thông tin này.
- **Khắc phục:** Chỉ đưa các claims tối thiểu cần thiết (`sub`, `role`, `scopes`, `exp`) vào JWT.

### 6. Thiếu Rate Limit và lỗi rò rỉ thời gian ở /auth/login - Rủi ro: MEDIUM
- **Mô tả:** Endpoint `/auth/login` là mục tiêu của Brute-force. Nếu không có Rate Limit, hacker có thể thử hàng triệu mật khẩu.
- **Kịch bản lộ:** Kẻ tấn công dùng wordlist để dò mật khẩu. Ngoài ra, nếu API trả về lỗi "Email không tồn tại" (nhanh) và "Sai mật khẩu" (chậm - do phải hash check), hacker có thể dựa vào thời gian phản hồi để liệt kê danh sách email hợp lệ (Timing Attack).
- **Khắc phục:** Áp dụng Rate Limit (VD: 5 lần/phút). Luôn trả về lỗi chung `401 Unauthorized` với thông báo "Email hoặc mật khẩu không đúng" bất kể sai ở bước nào.