from rest_framework import status
from typing import List
from ninja import Router
from django.shortcuts import get_object_or_404
from core.schemas import MessageOut
# 
from blog_course.models import Content
from core.authrztion import CustomAuth
from dna101blog.utlize.validations import get_user_profile
from blog_course.schemas import BlogIn, BlogOut, CourseIn, CourseOut, ContentIn
from dna101blog.utlize.custom_class import Error

blog_router = Router()
course_router = Router()
content_router = Router()

@blog_router.get("/get_all_blogs", response={200: List[BlogOut]})
def list_blogs(request):
    blogs = list(Content.objects.filter(content_type=Content.TypeChoices.BLOG))

    return status.HTTP_200_OK, blogs


@blog_router.get("/get_all_courses", response={200: List[BlogOut]})
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
    blog = get_object_or_404(Content, id=id)
    if blog.content_type != Content.TypeChoices.BLOG:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="there is no blog with such ID")

    return status.HTTP_200_OK, blog


@blog_router.get("/get_course_by_id/{id}", 
                 response={
                    200: CourseOut, 
                    404: MessageOut,
                    400:MessageOut,
                    },

                 )
def get_course(request, id: int):
    course = get_object_or_404(Content, id=id)
    if course.content_type != Content.TypeChoices.COURSE:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="there is no course with such ID")

    return status.HTTP_200_OK, course


def create_content(email, title, description, content, img, content_type):
    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message

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

    return status.HTTP_200_OK, blog


@blog_router.post("/create_course", 
                response={
                    200: CourseOut, 
                    404: MessageOut,
                    400:MessageOut,
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

    return status.HTTP_200_OK, course


@content_router.put("/update_content/{id}", 
                 response={
                     200: BlogOut,
                     }
                 )
def update_content(request, id: int, content_in: ContentIn):
    content = get_object_or_404(Content, id=id)

    content.title = content_in.title
    content.description = content_in.description
    content.content = content_in.content
    content.img = content_in.img

    content.save()

    return status.HTTP_200_OK, BlogOut(content)


@content_router.delete("/delete_content/{id}")
def delete_content(request, id: int):
    content = get_object_or_404(Content, id=id)
    content.delete()

    return status.HTTP_200_OK, MessageOut(detail="Blog deleted")


