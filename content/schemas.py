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
    img: Optional[str]

class ContentIn(ContentSchema):
    pass

class Contentshort(Schema):
    id: int
    profile: ContentProfile
    img: Optional[str]
    title: str
    description: str

class ContentOut(Contentshort):
    content: str


class NewContent(Contentshort):
    content_type: str

# Blog schema
class BlogSchema(ContentSchema):
    pass

class BlogIn(ContentSchema):
    pass

class BlogEdit(ContentSchema):
    id:int

class BlogShort(Contentshort):
    pass

class BlogOut(ContentOut):
    id: int


# Course schema
class CourseSchema(ContentSchema):
    pass

class CourseIn(ContentSchema):
    pass

class CourdeShort(Contentshort):
    pass

class CourseEdit(ContentSchema):
    id: int

class CourseOut(ContentOut):
    id: int

 