from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_login import LoginManager
from .enums import *

app = Flask(__name__)
app.secret_key = "\xb9\xd5\x97\xcc4\x81\xf8X\x98N\xde\xd6\x07?\xf5\x9f"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:0000@localhost/hoteldb?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['ROOT_PROJECT_PATH'] = app.root_path

db = SQLAlchemy(app=app)

admin = Admin(app=app, name="QUAN LY KHACH SAN", template_mode="bootstrap4")

login = LoginManager(app=app)
