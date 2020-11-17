from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView

from hotel import admin
from hotel.models import *






class ContactView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/contact.html')


class TypeModelView(ModelView):
    column_display_pk = True
    can_export = True


class RoomDetailModelView(ModelView):
    can_export = True


admin.add_view(RoomDetailModelView(RoomDetail, db.session))
admin.add_view(TypeModelView(Type, db.session))
admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Order, db.session))
admin.add_view(ModelView(Booking, db.session))
admin.add_view(ModelView(Invoice, db.session))
admin.add_view(ContactView(name='Contact'))
