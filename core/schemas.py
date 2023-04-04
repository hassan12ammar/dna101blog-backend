from pydantic import EmailStr, Field
from ninja import Schema


class MessageOut(Schema):
    detail: str

class UserIn(Schema):
    name: str
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)


class TokenOut(Schema):
    access: str


class UserOut(Schema):
    name: str
    email: EmailStr


class AuthOut(Schema):
    token: TokenOut
    user: UserOut


class SigninIn(Schema):
    email: EmailStr
    password: str

