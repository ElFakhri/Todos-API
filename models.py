from database import Base
from sqlalchemy import Column, String, Boolean, Integer, DateTime


class Todo(Base):
    __tablename__ = "todo"

    id = Column(Integer, primary_key=True)
    title = Column(String, index=True)
    created_date = Column(DateTime)
    last_updated_date = Column(DateTime)
    is_done = Column(Boolean, default=False)
    description = Column(String)


class User(Base):
    __tablename__ = "user"

    username = Column(String, unique=True)
    email = Column(String, primary_key=True)
    is_male = Column(Boolean)
    hashed_password = Column(String, nullable=False)
