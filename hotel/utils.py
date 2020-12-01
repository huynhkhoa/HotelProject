import  hashlib
from hotel.models import User
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
