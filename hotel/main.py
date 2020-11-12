from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/")
def main():
    return render_template("home.html")

@app.route("/hello/<name>/<int:year>")
def hello(name, year):
    if request.args.get("location") and request.args.get("email"):
        msg = "%s - %s" % (request.args["location"], request.args["email"])

    return "Hello %s; YEAR: %d; %s" % (name, year, msg)

@app.route("/login", methods=["get", "post"])
def login_user():
    if request.method == 'POST':
        username = request.form["un"]
        password = request.form["pass"]
        if username == "admin" and password == "123":
            return render_template("login.html", username=username, password=password)
        else:
            return "failed"

    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
