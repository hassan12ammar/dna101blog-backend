"""
URL configuration for dna101blog project.

The `urlpatterns` list routes URLs to views.
"""
from ninja import NinjaAPI
from django.urls import path
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
# local import
from core.controllers import auth_controller
from profile_.controllers import profile_controller
from content.controllers import blog_router, course_router, general_content
from .utlize.constant import DESCRIPTION


api = NinjaAPI(title="Blog Backend", 
                description=DESCRIPTION)
api.add_router("auth", auth_controller, tags=["Auth"])
api.add_router("profile", profile_controller, tags=["Profile"])
api.add_router("general content", general_content, tags=["General Content"])
api.add_router("blog", blog_router, tags=["Blog"])
api.add_router("course", course_router, tags=["Course"])

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
