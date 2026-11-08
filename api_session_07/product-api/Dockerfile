# bai 3 #

# ==========================================
# STAGE 1: BUILDER (Cài đặt thư viện)
# ==========================================
FROM python:3.12-slim AS builder
WORKDIR /build

# Copy requirements và cài vào 1 thư mục tạm
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ==========================================
# STAGE 2: RUNTIME (Chạy ứng dụng)
# ==========================================
FROM python:3.12-slim
WORKDIR /app

# Copy thư viện đã cài từ Stage 1 sang
COPY --from=builder /install /usr/local

# Copy toàn bộ source code
COPY . .

# Cấu hình PYTHONPATH để nhận diện thư mục src
ENV PYTHONPATH=/app/src
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Tạo user không phải root để bảo mật
RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app
USER app

EXPOSE 5000

# Chạy Migration tự động, sau đó khởi động Gunicorn
CMD flask --app wsgi db upgrade && gunicorn --bind 0.0.0.0:5000 wsgi:app