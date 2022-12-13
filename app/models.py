from .database import Base
from sqlalchemy import Column, String
from sqlalchemy_utils import EmailType



class User(Base):
    __tablename__ = 'User'
    id = Column(String, primary_key=True)
    full_name = Column(String)
    email_address = Column(EmailType)
