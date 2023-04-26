# built-in imports
import os
from typing import List
from uuid import uuid4
# third-party imports
from ninja import Body, File, Router, UploadedFile
from typing import Union
from rest_framework import status
from django.core.files.base import ContentFile

from dna101blog.utlize.constant import CONTENT_PER_PAGE
# local imports
from .models import Content
from core.schemas import MessageOut
from core.authrztion import CustomAuth
from dna101blog.utlize.custom_class import Error
from dna101blog.utlize.validations import get_user_profile, normalize_email
from .schemas import BlogIn, BlogOut, CourseIn, CourseOut, BlogEdit, CourseEdit


blog_router = Router()
course_router = Router()

@blog_router.get("/get_all_blogs/{page_number}", 
                 response={
                       200: List[BlogOut],
                       400: MessageOut
                       })
def list_blogs(request, page_number:int):
    # validate page number
    if page_number <= 0:
        return status.HTTP_400_BAD_REQUEST, MessageOut(
                detail="Invalid page number Has to be grater than 0")

    start = (page_number - 1) * CONTENT_PER_PAGE
    end = start + CONTENT_PER_PAGE

    blogs = Content.objects.filter(content_type=Content.TypeChoices.BLOG
            ).order_by("id")[start:end]

    return status.HTTP_200_OK, blogs


@course_router.get("/get_all_courses/{page_number}", 
                   response={
                       200: List[BlogOut],
                       400: MessageOut
                       })
def list_courses(request, page_number:int):
    # validate page number
    if page_number <= 0:
        return status.HTTP_400_BAD_REQUEST, MessageOut(
                detail="Invalid page number Has to be grater than 0")

    start = (page_number - 1) * CONTENT_PER_PAGE
    end = start + CONTENT_PER_PAGE

    courses = Content.objects.filter(content_type=Content.TypeChoices.COURSE
              ).order_by("id")[start:end]

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
        content_type=content_type,
    )

    # Save content picture if provided
    if img:
        content_.img.save(f'{content_type}-{title}-{uuid4()}.jpg', img)
    else: content_.img=img

    return content_


@blog_router.post("/create_blog", 
                response={
                    200: BlogOut, 
                    404: MessageOut,
                    400:MessageOut,
                    },
                auth=CustomAuth(),
                )
def create_blog(request, blog_in: BlogIn=Body(...), img: UploadedFile=File(None)):

    email = normalize_email(request.auth)
    blog = create_content(email, blog_in.title, 
                          blog_in.description, 
                          blog_in.content, 
                          img, 
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
def create_course(request, course_in: CourseIn=Body(...), img: UploadedFile=File(None)):

    email = normalize_email(request.auth)
    course = create_content(email, course_in.title, 
                          course_in.description, 
                          course_in.content, 
                          img, 
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
    
    # Save content picture if provided
    if img:
        # remove old img
        if img:
            os.remove(content_.img.path)
        # profile.img = img
        content_.img.save(f'{content_type}-{title}-{uuid4()}.jpg', img)

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
def edit_blog(request, blog_in: BlogEdit=Body(...), img: UploadedFile=File(None)):

    email = normalize_email(request.auth)
    blog = edit_content(blog_in.id, email, blog_in.title, 
                          blog_in.description, 
                          blog_in.content, 
                          img, 
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
def edit_course(request, course_in: CourseEdit=Body(...), img: UploadedFile=File(None)):

    email = normalize_email(request.auth)
    course = edit_content(course_in.id, email, course_in.title, 
                          course_in.description, 
                          course_in.content, 
                          img, 
                          Content.TypeChoices.COURSE)

    if isinstance(course, Error):
        return course.status, course.message

    return status.HTTP_200_OK, course


