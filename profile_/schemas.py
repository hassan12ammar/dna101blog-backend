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


class ProfileSchemaIn(ProfileSchema):
    pass


class ProfileSchemaOut(ProfileSchema):
    img: Optional[str] = None
    email: EmailStr
    
    @staticmethod
    def resolve_email(self):
        return self.user.email


class ProfileSchemaUpdate(ProfileSchemaIn):
    pass


class ProfileSchemaDelete(Schema):
    pass

