from flask import render_template, request, json, jsonify, redirect
from hotel import app, login
from flask_login import login_user
from hotel.admin import *
import hashlib


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

@app.route("/api/products")
def get_product_list():
    with open("data/products.json", encoding="utf-8") as f:
        products = json.load(f)

        return jsonify({"products": products})


@app.route("/login-admin", methods=["post", "get"])
def login_admin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = User.query.filter(User.username == username.strip(), User.password == password).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@login.user_loader
def user_load(user_id):
    return User.query.get(user_id)


if __name__ == "__main__":
    app.run(debug=True)
