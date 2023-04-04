# import libraries
from typing import List
from ninja import Router
from rest_framework import status
from django.contrib.auth import get_user_model
# import files
# import models
from profile_.models import Education, Experience, Profile
# import schemas
from core.schemas import MessageOut, UserOut
from profile_.schemas import ProfileSchema, ProfileSchemaDelete, ProfileSchemaIn, ProfileSchemaOut
# import functions
from dna101blog.utlize.validations import get_user, get_user_profile
# import custom classes
# from dna101blog.authrztion import CustomAuth
from dna101blog.utlize.custom_class import Error

User = get_user_model()


profile_controller = Router()


@profile_controller.get("get_all_users", response={
    200: List[UserOut],
    404: MessageOut,
    })
def get_all_users(request):
    users = User.objects.all()
    if users:
        return status.HTTP_200_OK, users
    return status.HTTP_404_NOT_FOUND, MessageOut(detail="No users found")


@profile_controller.get("all_profile", response={200: List[ProfileSchemaOut],
                                                 404: MessageOut,})
def all_profile(request):
    # get all profiles
    profile = Profile.objects.all().select_related('user')
    # check if profile is not empty
    if profile:
        return status.HTTP_200_OK, profile

    return status.HTTP_404_NOT_FOUND, MessageOut(detail="No profile found")


@profile_controller.get("get_profile/{email}", response={200: ProfileSchemaOut, 404: MessageOut,})
def get_profile(request, email):
    # normailze email
    norm_email = email.strip().lower().replace(" ", "")
    # check if user and profile exists
    profile = get_user_profile(norm_email)
    if isinstance(profile, Error):
        return profile.status, profile.message

    return status.HTTP_404_NOT_FOUND, MessageOut(detail="profile not found")

"""
@profile_controller.post("create_profile/{email}", response={200: ProfileSchemaOut, 404: MessageOut,})
def create_profile(request, email):
    # normailze email
    norm_email = email.strip().lower().replace(" ", "")
    # check if user and profile exists
    user = User.get_object_or_404(User, email=email)
"""

