# Nội dung bài 1#
import os   # thư viện đọc biến môi trường
class DefaultConfig:
    # Cấu hình mặc định cho ứng dụng Flask
    # Flask sẽ tự động đọc các thuộc tính bên trong class này thông qua lệnh app.config.from_object(DefaultConfig)
    SQLALCHEMY_DATABASE_URI = os.environ.get("DB_URL", "sqlite:///dev.db")  # no se ket nối đén database nào
    SQLALCHEMY_TRACK_MODIFICATIONS = False # tắt tự động theo dõi của sqlachemy để giảm tiêu tốn tài nguyên
    
    # Khóa bí mật để bảo vệ dữ liệu của ứng dụng, 
    # nếu không có biến môi trường SECRET_KEY thì sẽ sử dụng giá trị mặc định "dev-secret"
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret") # chìa kóa để flask mã hóa session/cookie
