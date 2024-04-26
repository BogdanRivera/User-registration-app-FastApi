from config.database import base
from sqlalchemy import Column, Integer, String, Boolean

class Users(base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    userName = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column (String)
    administrator = Column(Boolean)