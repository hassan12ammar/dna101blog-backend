from ninja import Schema
from typing import Optional

class BlogProfile(Schema):
    name: str
    title:str
    img: Optional[str]

class BlogCourseSchema(Schema):
    profile: BlogProfile
    title: str
    description: str
    content: str
    img: Optional[str]


# Blog schema
class BlogSchema(BlogCourseSchema):
    pass


# Course schema
class CourseSchema(BlogCourseSchema):
    pass

class BlogIn(BlogCourseSchema):
    pass

class CourseIn(BlogCourseSchema):
    pass

class BlogOut(BlogCourseSchema):
    id: int

class CourseOut(BlogCourseSchema):
    id: int

 