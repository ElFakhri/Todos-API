from pydantic import BaseModel, EmailStr
from datetime import datetime


# TODO SCHEMA ------------


class TodoBase(BaseModel):
    title: str
    description: str


class TodoCreate(TodoBase):
    pass


class TodoUpdate(TodoBase):
    pass


class Todo(TodoBase):
    id: int
    created_date: datetime
    last_updated_date: datetime
    is_done: bool
    owner_email: EmailStr

    class Config:
        from_attributes = True


# USER SCHEMA ---------------


class UserBase(BaseModel):
    username: str
    email: EmailStr
    is_male: bool


class UserCreate(UserBase):
    password: str


class User(UserBase):
    hashed_password: str


class UserLogin(BaseModel):
    username: str
    password: str
