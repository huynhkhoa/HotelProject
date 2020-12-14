from symbol import decorator

from flask import render_template, request, redirect, url_for, jsonify, session
from hotel import app, login, utils
from hotel.models import *
from flask_login import login_user, logout_user
from hotel.admin import *
import hashlib, os


@app.route("/")
def main():
    return render_template("home.html")


@app.route("/home")                          # toi page chu
def view_first_page():
    return render_template("home.html")


@app.route("/about")                         # toi page about
def view_about_page():
    return render_template("about.html")


@app.route("/contact")                       # toi page contact
def view_contact_page():
    return render_template("contact.html")


@app.route("/services")                      # toi page service
def view_services_page():
    return render_template("services.html")


@app.route("/book")                          # toi page booking
def view_book_page():
    return render_template('menu.html')


@app.route("/bill")                          # toi page bill
def view_bill():
    return render_template("bill.html")


@app.route("/booking")                        # toi page booking
def view_search_page():
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    roomdetails = utils.read_roomdetails(from_price=from_price,
                                         to_price=to_price)

    return render_template("booking.html", roomdetails=roomdetails)


@app.route("/search/<int:roomdetail_id>")    #xem thong tin chi tiet cac phong
def room_detail(roomdetail_id):
    roomdetail = utils.get_roomdetail_by_id(roomdetail_id=roomdetail_id)

    return render_template('room-detail.html',
                           roomdetail=roomdetail)


@app.route("/login", methods=['get', 'post'])    # toi page login
def login_admin():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password', '')
        password = str(hashlib.md5(password.encode("utf-8")).hexdigest())

        user = User.query.filter(User.username == username,
                                 User.password == password).first()

        if user:
            login_user(user=user)
    elif request.method == 'GET':
        print(request.url)
        return render_template('login.html')

    return redirect('/')


@app.route('/register', methods=['get', 'post'])         # toi page dang ky
def register():
    err_msg = ""
    if request.method == 'POST':             # gui data tu bieu mau register.html den server
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()        # băm password

        if password == confirm_password:
            if utils.add_user(name=name,
                              email=email,
                              phone=phone,
                              username=username,
                              password=password):
                return redirect('/admin')
        else:
            err_msg = "Password Error"

    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')                 # dang xuat tai khoan (chi xuat hien khi login thanh cong)
def logout_usr():
    logout_user()
    return redirect("/")


@app.route('/api/cart', methods=['post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    roomdetail_id = str(data.get('id'))
    roomdetail_name = data.get('name')
    price = data.get('price')

    cart = session['cart']
    if roomdetail_id in cart:                               # nếu sp đã có trong giỏ
        quan = cart[roomdetail_id]['quantity']
        cart[roomdetail_id]['quantity'] = int(quan) + 1
    else:                                                   # sp chưa có trong giỏ
        cart[roomdetail_id] = {
            "id": roomdetail_id,
            "name": roomdetail_name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart
    quan, price = utils.cart_stats(session['cart'])

    return jsonify({
        'total_quantity': quan,
        'total_amount': price
    })


@app.route('/payment', methods=['get', 'post'])                       #chức năng giỏ hàng
def payment():
    if request.method == 'POST':
        if utils.add_receipt(session.get('cart')):
            del session['cart']

            return jsonify({"message": "Payment added!!!"})

    quan, price = utils.cart_stats(session.get('cart'))
    cart_info = {
        'total_quantity': quan,
        'total_amount': price
    }
    return render_template('payment.html', cart_info=cart_info)


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
