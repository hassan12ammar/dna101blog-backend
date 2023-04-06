from ninja import Schema, Field
from typing import Optional


class ContentProfile(Schema):
    name: str
    title:str
    img: Optional[str]


class ContentSchema(Schema):
    title: str
    description: str
    content: str
    img: Optional[str]

class ContentIn(ContentSchema):
    pass

class ContentOut(Schema):
    profile: ContentProfile
    title: str
    description: str
    content: str
    img: Optional[str]


# Blog schema
class BlogSchema(ContentSchema):
    pass

class BlogIn(ContentSchema):
    pass

class BlogOut(ContentOut):
    id: int

# Course schema
class CourseSchema(ContentSchema):
    pass

class CourseIn(ContentSchema):
    pass

class CourseOut(ContentOut):
    id: int

 