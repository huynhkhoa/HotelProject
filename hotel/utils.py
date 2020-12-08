import hashlib, json
from hotel.models import *
from hotel import db


def add_user(name, email, phone, identity_card, username, password, avatar):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             phone=phone,
             identity_card=identity_card,
             username=username,
             password=password,
             avatar=avatar)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def cart_stats(cart):
    products = cart.values()

    quantity = sum([p['quantity'] for p in products])
    price = sum([p['price'] for p in products])

    return quantity, price


def read_roomdetails(from_price=None, to_price=None) -> object:

    roomdetails = RoomDetail.query

    if from_price and to_price:
        roomdetails = roomdetails.filter(RoomDetail.price.__gt__(from_price),
                                         RoomDetail.price.__lt__(to_price))

    return roomdetails.all()


def get_roomdetail_by_id(roomdetail_id):
    return RoomDetail.query.get(roomdetail_id)