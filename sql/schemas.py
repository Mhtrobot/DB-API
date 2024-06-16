from pydantic import BaseModel
from typing import Optional
from datetime import date, time

class UserBase(BaseModel):
    phone: Optional[str]
    first_name: str
    last_name: str
    national_code: str
    gender: str
    date_of_birth: date
    email: str
    home_phone: Optional[str]
    description: Optional[str]

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class UserModel(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class LoginData(BaseModel):
    email: str
    phone: str

class ItemBase(BaseModel):
    owner_id: int
    name: str
    price: float
    about: Optional[str]

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    item_id: int

    class Config:
        orm_mode = True

class TypeList(BaseModel):
    type_list_id: int
    name: Optional[str]

    class Config:
        orm_mode = True

class Type(BaseModel):
    type_id: int
    item_id: int
    type_list_id: int

    class Config:
        orm_mode = True

class LocationBase(BaseModel):
    state: str
    city: str
    exact_loc: str

class Location(LocationBase):
    location_id: int
    item_id: int
    class Config:
        orm_mode = True
class LocationCreate(LocationBase):
    pass

class Feature(BaseModel):
    feature_id: int
    item_id: int
    name: str
    more_detail: Optional[str]

    class Config:
        orm_mode = True

class OpenClose(BaseModel):
    open_close_id: int
    open_time: time
    close_time: time
    item_id: int

    class Config:
        orm_mode = True

class Rule(BaseModel):
    rule_id: int
    item_id: int
    name: str
    value: bool

    class Config:
        orm_mode = True

class Rating(BaseModel):
    rating_id: int
    item_id: int
    total_rate: int
    user_id: int

    class Config:
        orm_mode = True

class Rate(BaseModel):
    rate_id: int
    rate_title: str
    rate: int
    item_id: int
    user_id: int

    class Config:
        orm_mode = True

class Property(BaseModel):
    property_id: int
    item_id: int
    status: str

    class Config:
        orm_mode = True

class ItemDescription(BaseModel):
    item_desc_id: int
    item_id: int
    capacity: int
    room: int
    single_bed: int
    double_bed: int
    shower: int
    foreign_wc: int
    persian_wc: int
    caption: str

    class Config:
        orm_mode = True

class Message(BaseModel):
    message_id: int
    sender_id: int
    receiver_id: int
    item_id: int
    text: str

    class Config:
        orm_mode = True

class Like(BaseModel):
    user_id: int
    item_id: int

    class Config:
        orm_mode = True

class CommentSection(BaseModel):
    comment_id: int
    item_id: int
    user_id: int
    comment: str

    class Config:
        orm_mode = True

class Reservation(BaseModel):
    res_id: int
    renter_id: int
    item_id: int
    entry_date: date
    exit_date: date
    passengers_number: int
    final_price: float

    class Config:
        orm_mode = True

class Application(BaseModel):
    app_id: int
    res_id: int
    status: str

    class Config:
        orm_mode = True

class Invoice(BaseModel):
    invoice_id: int
    app_id: int
    user_id: int
    date: date
    discount: float
    status: str

    class Config:
        orm_mode = True

class Payment(BaseModel):
    payment_id: int
    invoice_id: int
    date: date

    class Config:
        orm_mode = True

class InvoiceLine(BaseModel):
    invoice_line_id: int
    payment_id: int

    class Config:
        orm_mode = True