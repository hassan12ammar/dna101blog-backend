# import libraries
from typing import List
from ninja import Schema
from pydantic import EmailStr, Field
# import files
from core.schemas import UserOut

class skillSchema(Schema):
    name: str


class ProfileSchema(Schema):
    title: str
    bio: str = None
    img: str = None
    skills: List[skillSchema]


class ProfileSchemaIn(ProfileSchema):
    user:  UserOut = Field(alias='user')


class ProfileSchemaOut(ProfileSchema):
    name: str
    email: EmailStr


class ProfileSchemaUpdate(ProfileSchemaIn):
    pass


class ProfileSchemaDelete(Schema):
    email: EmailStr

