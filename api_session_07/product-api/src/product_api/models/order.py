#Bài 2#

from datetime import datetime
from sqlalchemy import Integer, ForeignKey, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..extensions import db

class Order(db.Model): # một bảng đơn hàng trong database, kế thừa từ db.Model
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    
    # Mối quan hệ 1-N: 1 Order có nhiều OrderItem
    items: Mapped[list["OrderItem"]] = relationship(back_populates="order", cascade="all, delete-orphan")

class OrderItem(db.Model): #chi tiết đơn hàng với số lượng và giá
    __tablename__ = "order_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"), nullable=False)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Liên kết ngược lại để lấy thông tin
    order: Mapped["Order"] = relationship(back_populates="items")
    product = relationship("Product") # Lấy thông tin sản phẩm