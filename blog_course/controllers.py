from rest_framework import status
from typing import List
from ninja import Router, Schema
from django.shortcuts import get_object_or_404
# 
from blog_course.models import Blog
from blog_course.schemas import BlogIn, BlogOut

blog_router = Router()
course_router = Router()

class BlogId(Schema):
    id: int

@blog_router.get("/get_all_blogs", response=List[BlogOut])
def list_blogs(request):
    blogs = list(Blog.objects.all())
    print(blogs)
    print(blogs[0].profile.user.name)

    return list(Blog.objects.all())
    blogs = Blog.objects.all()
    return [BlogOut.from_orm(blog) for blog in blogs]


@blog_router.get("/blog_by_id/{id}", response=BlogOut)
def get_blog(request, id: int):
    blog = get_object_or_404(Blog, id=id)

    return BlogOut.from_orm(blog)


@blog_router.post("/create_blog", response=BlogOut)
def create_blog(request, blog_in: BlogIn):
    blog = Blog.objects.create(
        profile=request.auth.user.profile,
        title=blog_in.title,
        description=blog_in.description,
        content=blog_in.content,
        img=blog_in.img,
    )
    return BlogOut.from_orm(blog)


@blog_router.put("/update_blog/{id}", response=BlogOut)
def update_blog(request, id: int, blog_in: BlogIn):
    blog = get_object_or_404(Blog, id=id)
    blog.title = blog_in.title
    blog.description = blog_in.description
    blog.content = blog_in.content
    blog.img = blog_in.img
    blog.save()
    return BlogOut.from_orm(blog)

@blog_router.delete("/delete_blog/{id}")
def delete_blog(request, id: int):
    blog = get_object_or_404(Blog, id=id)
    blog.delete()
    return {"message": "Blog deleted"}



