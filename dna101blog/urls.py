"""
URL configuration for dna101blog project.

The `urlpatterns` list routes URLs to views.
"""
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

# from core.controllers import 
# from blog_course.controllers import 

api = NinjaAPI(title="Blog Backend", 
                description="Backend for Blog and Courses website using Django and Ninja")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
]

