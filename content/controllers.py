# built-in imports
from typing import List
# third-party imports
from ninja import Router
from typing import Union
from rest_framework import status
# local imports
from .models import Content
from core.schemas import MessageOut
from core.authrztion import CustomAuth
from dna101blog.utlize.custom_class import Error
from dna101blog.utlize.validations import get_user_profile
from .schemas import BlogIn, BlogOut, CourseIn, CourseOut, BlogEdit, CourseEdit


blog_router = Router()
course_router = Router()

@blog_router.get("/get_all_blogs", response={200: List[BlogOut]})
def list_blogs(request):
    blogs = list(Content.objects.filter(content_type=Content.TypeChoices.BLOG))

    return status.HTTP_200_OK, blogs


@course_router.get("/get_all_courses", response={200: List[BlogOut]})
def list_courses(request):
    courses = list(Content.objects.filter(content_type=Content.TypeChoices.COURSE))

    return status.HTTP_200_OK, courses


@blog_router.get("/get_blog_by_id/{id}", 
                response={
                    200: BlogOut, 
                    404: MessageOut,
                    400:MessageOut,
                    },
                 )
def get_blog(request, id: int):
    """ Get Blog By it's ID """
    blog = Content.objects.filter(id=id, content_type=Content.TypeChoices.BLOG).first()
    if not blog:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail=f"Could not find Blog with the given ID {id}")

    return status.HTTP_200_OK, blog


@course_router.get("/get_course_by_id/{id}", 
                 response={
                    200: CourseOut, 
                    404: MessageOut,
                    400:MessageOut,
                    },
                 )
def get_course(request, id: int):
    """ Get Course By it's ID """
    course = Content.objects.filter(id=id, content_type=Content.TypeChoices.COURSE).first()
    if not course:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail=f"Could not find Course with the given ID {id}")

    return status.HTTP_200_OK, course


def create_content(email, title, description, content, img, content_type) -> Union[Content, Error]:

    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile

    content_ = Content.objects.create(
        profile=profile,
        title=title,
        description=description,
        content=content,
        img=img,
        content_type=content_type,
    )
    
    return content_


@blog_router.post("/create_blog", 
                response={
                    200: BlogOut, 
                    404: MessageOut,
                    400:MessageOut,
                    },
                auth=CustomAuth(),
                )
def create_blog(request, blog_in: BlogIn):

    email = request.auth
    blog = create_content(email, blog_in.title, 
                          blog_in.description, 
                          blog_in.content, 
                          blog_in.img, 
                          Content.TypeChoices.BLOG)
    
    if isinstance(blog, Error):
        return blog.status, blog.message

    return status.HTTP_200_OK, blog


@course_router.post("/create_course", 
                response={
                    200: CourseOut, 
                    404:MessageOut,
                    400: MessageOut,
                    },
                auth=CustomAuth(),
                )
def create_course(request, course_in: CourseIn):

    email = request.auth
    course = create_content(email, course_in.title, 
                          course_in.description, 
                          course_in.content, 
                          course_in.img, 
                          Content.TypeChoices.COURSE)

    if isinstance(course, Error):
        return course.status, course.message

    return status.HTTP_200_OK, course


def edit_content(id, email, title, description, content, img, content_type) -> Union[Content, Error]:

    try:
        content_ = Content.objects.get(id=id)
    except:
        return Error(status.HTTP_400_BAD_REQUEST, 
                     MessageOut(detail=f"Could not find content with the given ID {id}"))

    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message
    
    if profile != content_.profile:
        return Error(status.HTTP_401_UNAUTHORIZED, 
                     MessageOut(detail=f"You are not authorized to edit this {content_type}"))

    if content_.content_type != content_type:
        return Error(status.HTTP_400_BAD_REQUEST, 
                     MessageOut(detail=f"Could not find {content_type} with the given ID {id}"))

    # update the fields
    content_.title = title
    content_.description = description
    content_.content = content
    content_.img = img
    # save the changes
    content_.save()

    return content_


@blog_router.put("/edit_blog", 
                response={
                    200: BlogOut, 
                    400:MessageOut,
                    401: MessageOut,
                    },
                auth=CustomAuth(),
                )
def edit_blog(request, blog_in: BlogEdit):

    email = request.auth
    blog = edit_content(blog_in.id, email, blog_in.title, 
                          blog_in.description, 
                          blog_in.content, 
                          blog_in.img, 
                          Content.TypeChoices.BLOG)

    if isinstance(blog, Error):
        return blog.status, blog.message

    return status.HTTP_200_OK, blog


@course_router.put("/edit_course", 
                response={
                    200: CourseOut, 
                    400:MessageOut,
                    401: MessageOut,
                    },
                auth=CustomAuth(),
                )
def edit_course(request, course_in: CourseEdit):

    email = request.auth
    course = edit_content(course_in.id, email, course_in.title, 
                          course_in.description, 
                          course_in.content, 
                          course_in.img, 
                          Content.TypeChoices.COURSE)

    if isinstance(course, Error):
        return course.status, course.message

    return status.HTTP_200_OK, course


