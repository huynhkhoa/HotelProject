from sqlalchemy import Column, Integer, Float, \
    String, ForeignKey, Date, Boolean
from hotel import db
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_login import UserMixin


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    note = Column(String(255), nullable=True)

    roomdetails = relationship('RoomDetail', backref='type', lazy=True)

    def __str__(self):
        return self.name


class RoomDetail(db.Model):
    __tablename__ = "roomdetail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    max_guess = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    bookings = relationship('Booking', backref='type', lazy=True)

    def __str__(self):
        return self.name


class User(db.Model, UserMixin):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=True)
    identity_card = Column(Integer, nullable=True)
    foregin = Column(Boolean, nullable=True)
    active = Column(Boolean, default=True)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    orders = relationship('Order', backref='type', lazy=True)
    invoices = relationship('Invoice', backref='type', lazy=True)

    def __str__(self):
        return self.name


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_arrive = Column(Date, default=datetime.now())
    NoDay = Column(Integer, nullable=False)
    noguess = Column(Integer, nullable=False)
    NoRoom = Column(Integer, nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(String(50), primary_key=True, autoincrement=False)
    roomdetail_id = Column(Integer, ForeignKey(RoomDetail.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)

    def __str__(self):
        return self.name


class Invoice(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    joined_date = Column(Date, default=datetime.now())

    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)

    user_id = Column(Integer, ForeignKey(User.id), nullable=False)

    def __str__(self):
        return self.name


if __name__ == "__main__":
    db.create_all()
