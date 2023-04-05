# import libraries
from typing import List, Optional
from ninja import Schema
from pydantic import EmailStr

class skillSchema(Schema):
    name: str


class ProfileSchema(Schema):
    name: str
    title: str
    bio: Optional[str] = None
    skills: Optional[List[skillSchema]]
    img: Optional[str]


class ProfileSchemaIn(ProfileSchema):
    email: str


class ProfileSchemaOut(ProfileSchema):
    email: str

class ProfileSchemaUpdate(ProfileSchemaIn):
    pass


class ProfileSchemaDelete(Schema):
    email: EmailStr

