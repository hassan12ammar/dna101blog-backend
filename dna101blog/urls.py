"""
URL configuration for dna101blog project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from core.controllers import auth_controller
from blog_course.controllers import blog_router, course_router, content_router
from profile_.controllers import profile_controller

api = NinjaAPI(title="Blog Backend", 
                description="Backend for Blog and Courses website using Django and Ninja")
api.add_router("auth", auth_controller, tags=["Auth"])
api.add_router("profile", profile_controller, tags=["Profile"])
api.add_router("blog", blog_router, tags=["Blog"])
api.add_router("course", course_router, tags=["Course"])
api.add_router("content", content_router, tags=["Content"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

