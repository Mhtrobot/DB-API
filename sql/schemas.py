from pydantic import BaseModel
from typing import Optional
from datetime import date

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