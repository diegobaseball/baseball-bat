import datetime
from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str
    password: str
    player: str
    birthdate: str
    gender: str
    status: str


class requestdetails(BaseModel):
    username: str
    password: str


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str


class changepassword(BaseModel):
    username: str
    old_password: str
    new_password: str


class TokenCreate(BaseModel):
    username: str
    access_token: str
    refresh_token: str
    status: bool
    created_date: datetime.datetime
