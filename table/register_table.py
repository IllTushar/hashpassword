from engine.db_connection import Base
from sqlalchemy import Column, Integer, String


class Registration(Base):
    __tablename__ = 'UserProfile'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
