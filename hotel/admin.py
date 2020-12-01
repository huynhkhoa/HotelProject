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


class LogoutView(BaseView):
    @expose("/")
    def index(self):
        logout_user()

        return redirect("/")

    def is_accessible(self):
        return current_user.is_authenticated


class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')

    def is_accessible(self):
        return current_user.is_authenticated


class TypeModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class RoomDetailModelView(ModelView):
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class UserModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class OrderModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class BookingModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


class InvoiceModelView(ModelView):
    column_display_pk = True
    can_export = True

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(RoomDetailModelView(RoomDetail, db.session))
admin.add_view(TypeModelView(Type, db.session))
admin.add_view(UserModelView(User, db.session))
admin.add_view(OrderModelView(Order, db.session))
admin.add_view(BookingModelView(Booking, db.session))
admin.add_view(InvoiceModelView(Invoice, db.session))
admin.add_view(LogoutView(name='Logout'))
admin.add_view(ContactView(name='Contact'))
