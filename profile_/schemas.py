# import libraries
from ninja import Schema
from pydantic import EmailStr
from typing import List, Optional

class SkillSchema(Schema):
    name: str


class ProfileSchema(Schema):
    name: str
    title: str
    bio: Optional[str] = None
    skills: Optional[List[SkillSchema]]
    img: Optional[str] = None


class ProfileSchemaIn(ProfileSchema):
    pass


class ProfileSchemaOut(ProfileSchema):
    email: EmailStr


class ProfileSchemaUpdate(ProfileSchemaIn):
    pass


class ProfileSchemaDelete(Schema):
    pass

