from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from  flask_login import current_user

from hotel import admin
from hotel.models import *
import hashlib


class AuthenticatedView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated


class UserModelView(ModelView):
    column_display_pk = True
    column_labels = dict(name="Tên người dùng"
                         , user_name="Tên đăng nhập", pass_word="Mật khẩu", roles="Vai trò")
    form_excluded_columns = ['user1', 'user2']

    def on_model_change(self, form, User, is_created=False):
        User.pass_word = hashlib.md5(User.pass_word.encode('utf-8')).hexdigest()



class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


class TypeModelView(AuthenticatedView):
    column_display_pk = True
    can_export = True


class RoomDetailModelView(ModelView):
    can_export = True


admin.add_view(RoomDetailModelView(RoomDetail, db.session))
admin.add_view(TypeModelView(Type, db.session))
admin.add_view(UserModelView(User, db.session, name="User"))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Booking, db.session))
admin.add_view(ModelView(Invoice, db.session))
admin.add_view(ContactView(name='Contact'))
