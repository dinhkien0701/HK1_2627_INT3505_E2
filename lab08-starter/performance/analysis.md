# Lab 4 — Phân tích kết quả

| Kịch bản | Users | Spawn rate | Duration | p95 (ms) | Failure rate | RPS |
|---|---:|---:|---:|---:|---:|---:|
| A | 10 | 2 | 30s | 8 | 0.00% | 5.04 |
| B | 50 | 5 | 60s | 10 | 0.14% | 23.66 |
| C | 200 | 50 | 30s | 190 | 0.11% | 97.29 |

1. **Kịch bản C có p95 cao nhất**, ở mức 190 ms, so với 8 ms ở A và 10 ms ở B.
   Khi tăng lên 200 users và spawn rate 50 users/giây, Flask development server và SQLite
   phải xử lý nhiều request đồng thời hơn. Vì vậy độ trễ ở đuôi phân phối tăng mạnh; p99
   của C là 340 ms, trong khi p99 của A và B lần lượt là 12 ms và 19 ms.

2. Failure chỉ xuất hiện ở endpoint `GET /books?year={year}`, vì đây là nơi code cố tình
   gọi `response.failure()` với xác suất 1%. Các failure này là lỗi đánh dấu phía client
   Locust, không phải HTTP 500 do Flask trả về. CSV ghi nhận 0 failure ở A, 2/1,397
   request ở B (0.14%), và 3/2,824 request ở C (0.11%). Không có exception server
   được ghi nhận.

3. Cả ba kịch bản đều đạt SLO giả định p95 < 300 ms: A = 8 ms, B = 10 ms, C = 190 ms.
   Tuy nhiên, C có p99 = 340 ms nên vẫn có một phần request vượt 300 ms. Đây chỉ là
   phép đo thực hành trên Flask development server, SQLite và một máy cá nhân; kết quả
   không đại diện cho production, không có network latency thực tế và chưa kiểm tra
   nhiều worker hoặc nhiều máy phát tải.

4. Để kiểm chứng connection pool giới hạn ở 5, chạy lại cùng một kịch bản (đặc biệt là C)
   với cấu hình pool cố định ở 5, giữ nguyên users, spawn rate và duration. So sánh
   `reports/*_stats.csv` trước và sau theo p95, p99, RPS, failure rate và thời gian
   của từng endpoint. Nếu pool trở thành nút thắt, khi số request đồng thời vượt 5 sẽ
   thấy p95/p99 và thời gian chờ tăng, RPS giảm hoặc xuất hiện lỗi timeout/pool timeout.

> Số liệu trong bảng lấy từ các file CSV của lần chạy tương ứng. Không khẳng định
> hiệu năng production từ SQLite + Flask development server trên máy cá nhân.
