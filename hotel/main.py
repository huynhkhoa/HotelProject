from flask import render_template, request, redirect, url_for, jsonify
from hotel import app, login, utils
from hotel.models import User
from flask_login import login_user, logout_user
from hotel.admin import *
import hashlib, os


@app.route("/")
def main():
    return render_template("home.html")


@app.route("/home.html")
def view_first_page():
    return render_template("home.html", title="home")


@app.route("/about.html")
def view_about_page():
    return render_template("about.html", title="about")


@app.route("/contact.html")
def view_contact_page():
    return render_template("contact.html", title="contact")


@app.route("/services.html")
def view_services_page():
    return render_template("services.html", title="services")


@app.route("/book.html")
def view_product_page():
    return render_template("book.html", title="product")


@app.route("/login", methods=['get', 'post'])
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


@app.route('/register', methods=['get', 'post'])
def register():
    err_msg = ''
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        identity_card = request.form.get('identity_card')
        username = request.form.get('username')
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if password == confirm_password:
            avatar = request.files["avatar"]
            avatar_path = 'images/upload/%s' % avatar.filename
            avatar.save(os.path.join(app.config['ROOT_PROJECT_PATH'],
                                     'static/', avatar_path))

            if utils.add_user(name=name, email=email, phone=phone, identity_card=identity_card, username=username,
                              password=password, avatar=avatar_path):
                return redirect('/admin')
        else:
            err_msg = "Mật khẩu KHÔNG khớp!"

    return render_template('register.html', err_msg=err_msg)


@app.route('/logout')
def logout_usr():
    logout_user()
    return redirect("/")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
