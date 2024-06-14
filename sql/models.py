from sqlalchemy import Column, Integer, String, TEXT, CHAR, Date, DECIMAL, ForeignKey, CheckConstraint, TIME, BOOLEAN, \
    DATE
from sqlalchemy.orm import relationship

from .database import Base

class USER(Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, index=True)
    phone = Column(String(11), nullable=True)
    first_name = Column(String(20), nullable=False)
    last_name = Column(String(20), nullable=False)
    national_code = Column(CHAR(10), nullable=False)
    gender = Column(CHAR(1), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    email = Column(String(50), nullable=False)
    home_phone = Column(String(11), nullable=True)
    description = Column(TEXT, nullable=True)

class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)
    about = Column(TEXT)

    owner = relationship("User", back_populates="items")
    locations = relationship("Location", back_populates="item")

class TypeList(Base):
    __tablename__ = 'type_list'

    type_list_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255))

class Type(Base):
    __tablename__ = 'type'

    type_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    type_list_id = Column(Integer, ForeignKey('type_list.type_list_id'), nullable=False)

    item = relationship("Item")
    type_list = relationship("TypeList")

class Location(Base):
    __tablename__ = 'location'

    location_id = Column(Integer, primary_key=True, index=True)
    state = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False)
    exact_loc = Column(String(255), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)

    item = relationship("Item", back_populates="locations")

class Feature(Base):
    __tablename__ = 'features'

    feature_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    name = Column(String(255), nullable=False)
    more_detail = Column(TEXT)

    item = relationship("Item")

class OpenClose(Base):
    __tablename__ = 'open_close'

    open_close_id = Column(Integer, primary_key=True, index=True)
    open_time = Column(TIME, nullable=False)
    close_time = Column(TIME, nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)

    item = relationship("Item")

class Rule(Base):
    __tablename__ = 'rules'

    rule_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    name = Column(String(255), nullable=False)
    value = Column(BOOLEAN, nullable=False)

    item = relationship("Item")

class Rating(Base):
    __tablename__ = 'ratings'

    rating_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    total_rate = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    item = relationship("Item")
    user = relationship("User")

class Rate(Base):
    __tablename__ = 'rates'

    rate_id = Column(Integer, primary_key=True, index=True)
    rate_title = Column(String(255), nullable=False)
    rate = Column(Integer, nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)

    item = relationship("Item")
    user = relationship("User")

class Property(Base):
    __tablename__ = 'properties'

    property_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    status = Column(String(255), nullable=False)

    item = relationship("Item")

class ItemDescription(Base):
    __tablename__ = 'item_description'

    item_desc_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    capacity = Column(Integer, nullable=False)
    room = Column(Integer, nullable=False)
    single_bed = Column(Integer, nullable=False)
    double_bed = Column(Integer, nullable=False)
    shower = Column(Integer, nullable=False)
    foreign_wc = Column(Integer, nullable=False)
    persian_wc = Column(Integer, nullable=False)
    caption = Column(String(255), nullable=False)

    item = relationship("Item")

class Message(Base):
    __tablename__ = 'messages'

    message_id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    receiver_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    text = Column(TEXT, nullable=False)

    sender = relationship("User", foreign_keys=[sender_id])
    receiver = relationship("User", foreign_keys=[receiver_id])
    item = relationship("Item")

class Like(Base):
    __tablename__ = 'likes'

    like_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)

    user = relationship("User")
    item = relationship("Item")

class CommentSection(Base):
    __tablename__ = 'comment_section'

    comment_id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    comment = Column(TEXT, nullable=False)

    item = relationship("Item")
    user = relationship("User")

class Reservation(Base):
    __tablename__ = 'reservations'

    res_id = Column(Integer, primary_key=True, index=True)
    renter_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    item_id = Column(Integer, ForeignKey('items.item_id'), nullable=False)
    entry_date = Column(DATE, nullable=False)
    exit_date = Column(DATE, nullable=False)
    passengers_number = Column(Integer, nullable=False)
    final_price = Column(DECIMAL(10, 2), nullable=False)

    renter = relationship("User")
    item = relationship("Item")

class Application(Base):
    __tablename__ = 'applications'

    app_id = Column(Integer, primary_key=True, index=True)
    res_id = Column(Integer, ForeignKey('reservations.res_id'), nullable=False)
    status = Column(String, nullable=False)

    reservation = relationship("Reservation")

class Invoice(Base):
    __tablename__ = 'invoice'

    invoice_id = Column(Integer, primary_key=True, index=True)
    app_id = Column(Integer, ForeignKey('applications.app_id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    date = Column(DATE, nullable=False)
    discount = Column(DECIMAL(10, 2), nullable=False)
    status = Column(String, nullable=False)

    application = relationship("Application")
    user = relationship("User")

class Payment(Base):
    __tablename__ = 'payment'

    payment_id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey('invoice.invoice_id'), nullable=False)
    date = Column(DATE, nullable=False)

    invoice = relationship("Invoice")

class InvoiceLine(Base):
    __tablename__ = 'invoice_line'

    invoice_line_id = Column(Integer, primary_key=True, index=True)
    payment_id = Column(Integer, ForeignKey('payment.payment_id'), nullable=False)

    payment = relationship("Payment")