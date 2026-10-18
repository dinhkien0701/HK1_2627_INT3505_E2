from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import mapped_column, relationship

db = SQLAlchemy()

class Category(db.Model):
    __tablename__ = 'categories'
    id = mapped_column(db.Integer, primary_key=True)
    name = mapped_column(db.String(100), nullable=False)
    slug = mapped_column(db.String(100), unique=True, nullable=False)

class Book(db.Model):
    __tablename__ = 'books'
    id = mapped_column(db.Integer, primary_key=True)
    title = mapped_column(db.String(200), nullable=False)
    isbn = mapped_column(db.String(20))
    price_vnd = mapped_column(db.Integer, default=0)
    stock = mapped_column(db.Integer, default=0)
    category_id = mapped_column(db.Integer, db.ForeignKey('categories.id'))

    category = relationship('Category')

    # Áp dụng slide trang 13: Prefix ID theo resource type
    def to_dict(self):
        return {
            "id": f"book_{self.id}",
            "title": self.title,
            "isbn": self.isbn,
            "price_vnd": self.price_vnd,
            "stock": self.stock,
            "category_id": self.category_id
        }