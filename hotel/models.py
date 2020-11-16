from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app import db


class Category(db.Model):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    products = relationship('Product', backref="category", lazy=True)


class Product(db.Model):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, default=0)
    image = Column(String(255), nullable=True)
    category_id = Column(Integer, ForeignKey(Category.id), nullable=False)



if __name__ == "__main__":
    db.create_all()
