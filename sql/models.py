from sqlalchemy import Column, Integer, String, Text, CHAR, Date
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
    description = Column(Text, nullable=True)