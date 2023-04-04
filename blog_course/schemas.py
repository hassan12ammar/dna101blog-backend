from ninja import schema

class BlofProfile(schema):
    name: str
    title:str
    img: str

class BlogCourseSchema(schema):
    profile: BlofProfile
    title: str
    description: str
    content: str
    img: str


