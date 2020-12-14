import hashlib, json
from hotel.models import *
from hotel import db


def add_user(name, email, phone, username, password):
    password = str(hashlib.md5(password.encode('utf-8')).hexdigest())
    u = User(name=name,
             email=email,
             phone=phone,
             username=username,
             password=password)
    try:
        db.session.add(u)
        db.session.commit()

        return True
    except Exception as ex:
        print(ex)
        return False


def read_roomdetails(from_price=None, to_price=None) -> object:
    roomdetails = RoomDetail.query

    if from_price and to_price:
        roomdetails = roomdetails.filter(RoomDetail.price.__gt__(from_price),
                                         RoomDetail.price.__lt__(to_price))

    return roomdetails.all()


def search_room_admin(name=None,
                      price=None,
                      guess=None,
                      description=None,
                      status=None,
                      image=None,
                      type_id=None):
    roomdetail = RoomDetail.query.all()
    kind = str(type_id)

    if name:
        roomdetail = filter(lambda r: r.name == name, roomdetail)

    if type_id:
        roomdetail = list(filter(lambda r: r.type_id.name == kind, roomdetail))

    if status:
        roomdetail = filter(lambda r: r.status.value == status, roomdetail)

    return roomdetail


def get_roomdetail_by_id(roomdetail_id):
    return RoomDetail.query.get(roomdetail_id)


def cart_stats(cart):
    if cart is None:
        return 0, 0

    roomdetails = cart.values()

    quantity = sum([r['quantity'] for r in roomdetails])
    price = sum([r['price'] * r['quantity'] for r in roomdetails])

    return quantity, price


def add_guess_foregin(date, guess, foregin):
    o = Order(date=date,
              guess=guess,
              foregin=foregin)
    try:
        db.session.add(o)
        db.session.commit()
        return True
    except Exception as ex:
        print(ex)
    return False


def add_receipt(cart):
    if cart:
        try:
            order = Order(order_id=1)
            db.session.add(order)

            for r in list(cart.values()):
                invoice = Invoice(roomdetail_id=int(r["id"]),
                                  order_id=order.id,
                                  price=float(r["price"]),
                                  quantity=r["quantity"])
                db.session.add(invoice)

            db.session.commit()

            return True
        except:
            pass

    return False

