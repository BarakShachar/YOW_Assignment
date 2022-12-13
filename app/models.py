from .database import Base
from sqlalchemy import Column, String, Integer
from sqlalchemy_utils import EmailType


class User(Base):
    __tablename__ = 'User'
    email = Column(EmailType, unique=True, primary_key=True, index=True)
    full_name = Column(String)
    id = Column(String)
    age = Column(Integer)

