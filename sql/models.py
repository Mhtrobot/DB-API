from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

URL_DATABASE = 'postgresql://postgres:admin@localhost:5432/Jabama'

engine = create_engine(URL_DATABASE, connect_args={'check_same_thread': False}, echo=True)

Base = declarative_base()