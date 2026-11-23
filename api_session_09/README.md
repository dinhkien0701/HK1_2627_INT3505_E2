# Bài tập tuần 9: API Versioning & Lifecycle Management

Bài tập gồm bốn cách triển khai versioning và quản lý vòng đời API.

## Bài 1: URI Path Versioning

- Dùng Flask Blueprint cho hai API: `/api/v1/users/<id>` và `/api/v2/users/<id>`.
- v1 trả về `full_name`, còn v2 trả về `first_name` và `last_name`.
- Dữ liệu người dùng được quản lý tập trung trong `users_data.py`.

## Bài 2: Header Versioning

- Dùng decorator `@api_version` và header `X-API-Version`.
- Một URL `/users/<id>` phục vụ nhiều phiên bản API.
- Response trả thêm header `X-API-Version-Served`.

## Bài 3: API Sunset

- Decorator `@deprecate_at` thêm header `Sunset`, `Deprecation` và `Link`.
- Sau thời điểm sunset, API trả về HTTP 410 Gone và hướng dẫn API thay thế.

## Bài 4: Blue-Green Routing

- Gateway chọn v1 hoặc v2 theo cohort, account allow-list và hash bucket.
- Tỷ lệ rollout được điều khiển bằng `V2_PERCENT`, hỗ trợ tăng dần lên 100%.

## Chạy ứng dụng

```bash
python app.py
```

API chạy tại `http://localhost:5000`.
