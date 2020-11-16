from sqlalchemy import Column, Integer, Float, \
    String, ForeignKey, Date
from datetime import datetime
from sqlalchemy.orm import relationship

from hotel import db


class Type(db.Model):
    __tablename__ = "type"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    note = Column(String(255), nullable=True)

    roomdetails = relationship('RoomDetail', backref='type', lazy=True)


class RoomDetail(db.Model):
    __tablename__ = "roomdetail"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    price = Column(Float, default=0)
    bed = Column(Integer, nullable=False)
    size = Column(String(50), nullable=False)
    max_guess = Column(Integer, nullable=True)
    description = Column(String(255), nullable=True)

    type_id = Column(Integer, ForeignKey(Type.id), nullable=False)
    bookings = relationship('Booking', backref='type', lazy=True)



class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    DoB = Column(Date, nullable=False)
    foregin = Column(String(50), nullable=False)
    username = Column(String(50), nullable=False)
    password = Column(String(50), nullable=False)

    orders = relationship('Order', backref='type', lazy=True)



class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date_arrive = Column(Date, default=datetime.now())
    NoDay = Column(Integer, nullable=False)
    noguess = Column(Integer, nullable=False)
    NoRoom = Column(Integer, nullable=False)

    bookings = relationship('Booking', backref='type', lazy=True)
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)


class Booking(db.Model):
    __tablename__ = "booking"
    id = Column(String(50), primary_key=True, autoincrement=False)
    roomdetail_id = Column(Integer, ForeignKey(RoomDetail.id), nullable=False)
    order_id = Column(Integer, ForeignKey(Order.id), nullable=False)




if __name__ == "__main__":
    db.create_all()
