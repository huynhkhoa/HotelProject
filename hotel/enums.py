import enum


class Status(enum.Enum):
    HaveRoom = "Phòng trống"
    NoRoom = "phòng đang dùng"


class CustomerType(enum.Enum):
    DomesticPassenger = "Khách nội địa"
    Foreigner = "Khách nước ngoài"

