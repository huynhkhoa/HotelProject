from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
import hashlib
from flask import redirect, request
from wtforms import validators

from hotel import admin, utils
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
    form_columns = ('name', 'price', 'note')
    column_labels = {"id": "Mã danh mục phòng",
                     "name": "Loại phòng",
                     "price": "Đơn giá",
                     "note": "Ghi chú"}

    def is_accessible(self):             # login thanh cong thi show TypeModelView
        return current_user.is_authenticated


class RoomDetailModelView(ModelView):    # ke thua RoomDetailModelView
    can_export = True
    column_display_pk = True
    column_labels = {"id": "Mã phòng",
                     "name": "Phòng",
                     "price": "Giá",
                     "guess": "Số lượng khách",
                     "status": "Trạng thái phòng",
                     "image": "Hình phòng",
                     "description": "Miêu tả",
                     "type": "Loại phòng"}

    def _status_formatter(view, context, model, name):
        if model.status:
            status = model.status.value
            return status
        else:
            return None

    column_formatters = {
        'status': _status_formatter
    }

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
    column_labels = {"id": "Mã phiếu thuê phòng",
                     "name": "Tên khách hàng",
                     "foregin": "Loại khách",
                     "identity_card": "CMND",
                     "address": "Địa chỉ",
                     "created_date": "Ngày đặt phòng",
                     "customer": "Loại khách",
                     "roomdetail": "Tên phòng",
                     "type": "Loại phòng",
                     "surcharge": "Phụ phí"}
    form_excluded_columns = ['invoice', 'User']

    def is_accessible(self):              # login thanh cong thi show OrderModelView
        return current_user.is_authenticated


class BookingModelView(ModelView):         # ke thua BookingModelView
    column_display_pk = True
    can_export = True
    column_labels ={"booking_id": "Mã đặt phòng"}

    def is_accessible(self):               # login thanh cong thi show BookingModelView
        return current_user.is_authenticated


class CustomerModelView(ModelView):         # ke thua CustomerModelView
    column_display_pk = True
    form_columns = ('customer_name', 'coefficient', 'note')
    column_labels = {"id": "Mã LK",
                     "customer_name": "Loại khách",
                     "coefficient": "Hệ số", "note": "Ghi chú"}

    def is_accessible(self):               # login thanh cong thi show BookingModelView
        return current_user.is_authenticated


class SurchargeModelView(AuthenticatedView):
    column_display_pk = True
    column_list = ["surcharge", "quantity"]
    column_labels = {"surcharge": "Phụ thu (%)",
                     "quantity": "Tổng số người"}
    form_excluded_columns = ['order']

    def is_accessible(self):
        return current_user.is_authenticated


class InvoiceModelView(ModelView):
    column_display_pk = True
    can_export = True
    column_labels = {"id": "Mã phiếu thuê",
                     "date": "Tổng ngày thuê",
                     "price": "Giá",
                     "order_id": "Mã PT",
                     "user_id": "Mã người dùng",
                     "quantity": "Tổng tiền"}

    form_excluded_columns = ['date_of_payment', 'value', 'price', 'User']

    def on_model_change(self, form, Invoice, is_created):
        roomdetail = RoomDetail.query.get(form.Order.data.booking_id)

        if roomdetail.status == Status.HaveRoom:
            raise validators.ValidationError("Phòng đã trả")

        if form.Order.data.RoomDetail.status == Status.NoRoom:
            roomdetail.status = Status.HaveRoom
            db.session.add(roomdetail)
            db.session.commit()

        if (datetime.now() - form.Order.data.created_date).days == 0:
            bill = (datetime.now().hour - form.Order.data.created_date.hour)
        else:
            bill= (datetime.now() - form.Order.data.created_date).days * 24

        hourOfPri = bill * form.Order.data.RoomDetail.price
        Invoice.created_date = bill / 24
        Invoice.value = hourOfPri
        Invoice.user_id = current_user.id

        if form.Order.data.Surcharge.surcharge == 0 and form.Order.data.Customer.coefficient == 0:
            Invoice.price = hourOfPri
        else:
            if form.Order.data.Surcharge.surcharge != 0 and form.data.Order.data.Customer.coefficient == 0:
                Invoice.price = hourOfPri + (hourOfPri * (form.Order.data.Surcharge.surcharge / 100))
            else:
                if form.Order.data.Surcharge.surcharge == 0 and form.Order.data.Customer.coefficient != 0:
                    Invoice.price = hourOfPri * form.Order.data.Customer.coefficient
                else:
                    if form.Order.data.Surcharge.surcharge != 0 and form.Order.data.Customer.coefficient != 0:
                        Invoice.price = hourOfPri * form.Order.data.Customer.coefficient + (
                                hourOfPri + (hourOfPri * (form.Order.data.Surcharge.surcharge / 100)))

    def is_accessible(self):                # login thanh cong thi show InvoiceModelView
        return current_user.is_authenticated


class SearchRoom(BaseView):
    @expose("/")
    def index(self):
        name = request.args.get("name")
        price = request.args.get("price")
        status = request.args.get("status")
        type_id = request.args.get("kind")

        return self.render("admin/search.html",
                           roomdetails=utils.search_room_admin(name=name,
                                                               price=price,
                                                               status=status,
                                                               type_id=type_id), status=Status)

    def is_accessible(self):                # login thanh cong thi show SearchRoom
        return current_user.is_authenticated


#add cac class vao page admin
admin.add_view(RoomDetailModelView(RoomDetail, db.session, name="Room"))
admin.add_view(TypeModelView(Type, db.session, name="Menu"))
admin.add_view(UserModelView(User, db.session, name="User"))
admin.add_view(OrderModelView(Order, db.session, name="Order form"))
admin.add_view(BookingModelView(Booking, db.session, name="Booking"))
admin.add_view(CustomerModelView(Customer, db.session, name="User type")) #loai khach
admin.add_view(SurchargeModelView(Surcharge, db.session, name="Extra Free")) #phu phi
admin.add_view(InvoiceModelView(Invoice, db.session, name="Invoice")) #hoa don
admin.add_view(SearchRoom(name="Search"))
admin.add_view(ContactView(name='Contact'))
admin.add_view(LogoutView(name='Logout'))
