from sqlalchemy import Column, Integer, Float, \
    String, ForeignKey, Date, Boolean, Enum, DateTime
from hotel import db, Status, CustomerType
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    note = Column(String(255), nullable=True)
    roomdetails = relationship('RoomDetail', backref='type', lazy=True)

    def __str__(self):
        return self.name + " - Giá: " + self.price.__str__()


class RoomDetail(db.Model):
    __tablename__ = "roomdetail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    guess = Column(Integer, nullable=True)
    status = Column(Enum(Status), nullable=True)
    image = Column(String(255))
    description = Column(String(500), nullable=True)
    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    bookings = relationship("Booking", backref='roomdetail', uselist=False)
    orders = relationship("Order", backref='roomdetail', lazy=True)

    def __str__(self):
        return self.name


class Customer(db.Model):
    __tablename__ = "Customer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_name = Column(String(50), nullable=False)
    coefficient = Column(Float, nullable=False)
    note = Column(String(50), nullable=False)
    orders = relationship('Order', backref="customer", lazy=True)

    def __str__(self):
        return self.customer_name


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    orders = relationship('Order', backref='type', lazy=True)

    def __str__(self):
        return self.name


class Surcharge(db.Model):
    __tablename__ = "surcharge"
    id = Column(Integer, primary_key=True, autoincrement=True)
    surcharge = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    orders = relationship('Order', backref="surcharge", lazy=True)

    def __str__(self):
        return self.quantity.__str__() + " Người - " + self.surcharge.__str__() + " %"


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    identity_card = Column(Integer, nullable=False)
    address = Column(String(50), nullable=False)
    created_date = Column(DateTime, default=datetime.today())
    customer_id = Column(Integer, ForeignKey(Customer.id), nullable=False)
    roomdetail_id = Column(Integer, ForeignKey(RoomDetail.id), nullable=False)
    surcharge_id = Column(Integer, ForeignKey(Surcharge.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    invoices = relationship("Invoice", backref='order', uselist=False)

    def __str__(self):
        return self.id.__str__() + " - Khách hàng: " + self.name.__str__() + " - CMND: " + self.identity_card.__str__()


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    roomdetail_id = Column(Integer, ForeignKey(RoomDetail.id), nullable=False)

    def __str__(self):
        return self.name


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Integer, nullable=False, default=0)
    price = Column(Float, default=0)
    value = Column(Integer, nullable=False, default=0)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    quantity = Column(Integer, default=0)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()
