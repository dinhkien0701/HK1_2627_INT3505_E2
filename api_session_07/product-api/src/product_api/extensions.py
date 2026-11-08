# Nội dung bài 1 #

# Khởi tạo các phần mở rộng hỗ trợ
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
db = SQLAlchemy()
migrate = Migrate()

'''
Migrate Hỗ trợ đồng bộ những thay đổi 
về cấu trúc Model Python 
vào Database TỰ ĐỘNG (so sánh sai lệch giữa database và model rồi tự sửa model).
'''

"""
SOLAlchemy là một thư viện ORM (Object Relational Mapping) cho Python, 
giúp kết nối và tương tác với cơ sở dữ liệu quan hệ một cách dễ dàng. 
Nó cung cấp một lớp trừu tượng để làm việc với cơ sở dữ liệu, 
cho phép thao tác với dữ liệu thông qua các đối tượng Python thay vì viết trực tiếp các câu lệnh SQL (raw sql).
"""