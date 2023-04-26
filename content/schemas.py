from ninja import Schema
from typing import Optional


class ContentProfile(Schema):
    name: str
    title:str
    img: Optional[str]


class ContentSchema(Schema):
    title: str
    description: str
    content: str

class ContentIn(ContentSchema):
    pass

class ContentOut(ContentSchema):
    profile: ContentProfile
    img: Optional[str]


# Blog schema
class BlogSchema(ContentSchema):
    pass

class BlogIn(ContentSchema):
    pass

class BlogEdit(ContentSchema):
    id:int

class BlogOut(ContentOut):
    id: int

# Course schema
class CourseSchema(ContentSchema):
    pass

class CourseIn(ContentSchema):
    pass

class CourseEdit(ContentSchema):
    id: int

class CourseOut(ContentOut):
    id: int

 