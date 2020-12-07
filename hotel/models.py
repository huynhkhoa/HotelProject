from sqlalchemy import Column, Integer, Float, \
    String, ForeignKey, Date, Boolean, Enum
from hotel import db
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as UserEnum


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    note = Column(String(255), nullable=True)

    roomdetails = relationship('RoomDetail', backref='type', lazy=True)

    def __str__(self):
        return self.name


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(Integer, primary_key=True, autoincrement=True)
    orders = relationship('Order', backref='booking', lazy=True)
    roomdetails = relationship('RoomDetail', backref='booking', lazy=True)

    def __str__(self):
        return self.name


class RoomDetail(db.Model):
    __tablename__ = "roomdetail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    max_guess = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)
    image = Column(String(255))
    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    booking_id = Column(Integer, ForeignKey(Booking.id))

    @property
    def __str__(self):
        return self.name


class UserRole(UserEnum):
    USER = 1
    ADMIN = 2


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    identity_card = Column(Integer, nullable=False)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)
    avatar = Column(String(100))
    user_role = Column(Enum(UserRole), default=UserRole.USER)

    orders = relationship('Order', backref='type', lazy=True)

    def __str__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_arrive = Column(Date, default=datetime.now())
    NoDay = Column(Integer, nullable=False)
    Noguess = Column(Integer, nullable=False)
    NoRoom = Column(Integer, nullable=False)
    foregin = Column(Boolean, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    booking_id = Column(Integer, ForeignKey(Booking.id), nullable=False)
    invoice = relationship("Invoice", backref='order', uselist=False)

    def __str__(self):
        return self.name


class Invoice(db.Model):
    __tablename__ = "invoice"
    id = Column(Integer, primary_key=True, autoincrement=True)
    joined_date = Column(Date, default=datetime.now())
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()
