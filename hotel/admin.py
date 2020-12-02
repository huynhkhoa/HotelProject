from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
import hashlib
from flask import redirect
from hotel import admin
from hotel.models import *


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class LogoutView(BaseView):              # ke thua LogoutView
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/")

    def is_accessible(self):             # login thanh cong thi show LogoutView
        return current_user.is_authenticated


class ContactView(BaseView):             # ke thua ContactView
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

    def is_accessible(self):             # login thanh cong thi show ContactView
        return current_user.is_authenticated


class TypeModelView(ModelView):          # ke thua TypeModelView
    column_display_pk = True
    can_export = True

    def is_accessible(self):             # login thanh cong thi show TypeModelView
        return current_user.is_authenticated


class RoomDetailModelView(ModelView):    # ke thua RoomDetailModelView
    can_export = True

    def is_accessible(self):             # login thanh cong thi show RoomDetailModelView
        return current_user.is_authenticated


class UserModelView(ModelView):          # ke thua UserModelView
    column_display_pk = True
    can_export = True

    def is_accessible(self):             # login thanh cong thi show UserModelView
        return current_user.is_authenticated


class OrderModelView(ModelView):          # ke thua OrderModelView
    column_display_pk = True
    can_export = True

    def is_accessible(self):              # login thanh cong thi show OrderModelView
        return current_user.is_authenticated


class BookingModelView(ModelView):         # ke thua BookingModelView
    column_display_pk = True
    can_export = True

    def is_accessible(self):               # login thanh cong thi show BookingModelView
        return current_user.is_authenticated


class InvoiceModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):                # login thanh cong thi show InvoiceModelView
        return current_user.is_authenticated


#add cac class vao page admin
admin.add_view(RoomDetailModelView(RoomDetail, db.session))
admin.add_view(TypeModelView(Type, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(BookingModelView(Booking, db.session))
admin.add_view(InvoiceModelView(Invoice, db.session))
admin.add_view(LogoutView(name='Logout'))
admin.add_view(ContactView(name='Contact'))
