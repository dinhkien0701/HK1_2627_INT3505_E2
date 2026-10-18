from flask import Flask
from models import db, Book, Category
from routes.books import books_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bookstore.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
app.register_blueprint(books_bp)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # --- Tạo dữ liệu mẫu để test (nếu DB trống) ---
        if not Category.query.first():
            cat1 = Category(name="Công nghệ", slug="tech")
            cat2 = Category(name="Văn học", slug="van-hoc")
            db.session.add_all([cat1, cat2])
            db.session.commit()

            books = [
                Book(title="Clean Code", isbn="9780132350884", price_vnd=450000, stock=10, category_id=cat1.id),
                Book(title="Design Patterns", isbn="9780201633610", price_vnd=600000, stock=5, category_id=cat1.id),
                Book(title="Tắt đèn", isbn="9786041234567", price_vnd=80000, stock=20, category_id=cat2.id),
                Book(title="Số đỏ", isbn="9786049876543", price_vnd=90000, stock=15, category_id=cat2.id),
                Book(title="Refactoring", isbn="9780134757599", price_vnd=550000, stock=8, category_id=cat1.id)
            ]
            db.session.add_all(books)
            db.session.commit()
            print("Đã tạo dữ liệu mẫu!")

    app.run(debug=True)