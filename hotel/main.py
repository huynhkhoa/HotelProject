from flask import render_template, request, redirect, url_for, jsonify
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
    return render_template('book.html')


@app.route("/bill")                          # toi page bill
def view_bill():
    return render_template("bill.html")


@app.route("/search")                        # toi page search
def view_search_page():
    from_price = request.args.get("from_price")
    to_price = request.args.get("to_price")

    roomdetails = utils.read_roomdetails(from_price=from_price,
                                         to_price=to_price)

    return render_template("search.html", roomdetails=roomdetails)


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
    err_msg = ''
    if request.method == 'POST':             # gui data tu bieu mau register.html den server
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        identity_card = request.form.get('identity_card')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()        # băm password

        if password == confirm_password:
            avatar = request.files["avatar"]
            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.config['ROOT_PROJECT_PATH'],
                                     'static/', avatar_path))

            if utils.add_user(name=name, email=email, phone=phone, identity_card=identity_card, username=username,
                              password=password, avatar=avatar_path):
                return redirect('/admin')
        else:
            err_msg = "Password Error"

    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')                 # dang xuat tai khoan (chi xuat hien khi login thanh cong)
def logout_usr():
    logout_user()
    return redirect("/")


@app.route('/api/cart', methods=['get','post'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = {}

    data = request.json
    product_id = str(data.get('id'))
    product_name = data.get('name')
    price = data.get('price')

    cart = session['cart']
    if product_id in cart: # nếu sp đã có trong giỏ
        quan = cart[product_id]['quantity']
        cart[product_id]['quantity'] = int(quan) + 1
    else: # sp chưa có trong giỏ
        cart[product_id] = {
            "id": product_id,
            "name": product_name,
            "price": price,
            "quantity": 1
        }

    session['cart'] = cart
    quan, price = utils.cart_stats(session['cart'])

    return jsonify({
        'total_quantity': quan,
        'total_amount': price
    })

@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
