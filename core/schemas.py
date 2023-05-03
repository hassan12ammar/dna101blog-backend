from ninja import Schema
from pydantic import EmailStr, Field

from profile_.models import Profile

class MessageOut(Schema):
    detail: str

class UserIn(Schema):
    email: EmailStr
    password1: str = Field(min_length=8)
    password2: str = Field(min_length=8)
    name: str


class TokenOut(Schema):
    access: str


class UserOut(Schema):
    email: EmailStr
    name: str
    
    @staticmethod
    def resolve_name(self):
        return Profile.objects.get(user=self).name


class AuthOut(Schema):
    token: TokenOut
    user: UserOut


class SigninIn(Schema):
    email: EmailStr
    password: str

class SigninUpOut(AuthOut):
    name: str
