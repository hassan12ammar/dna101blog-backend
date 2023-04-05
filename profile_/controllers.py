# import libraries
from typing import List
from ninja import Router
from rest_framework import status
from django.contrib.auth import get_user_model
# import files
# import models
from profile_.models import Profile, Skill
# import schemas
from core.schemas import MessageOut, UserOut
from profile_.schemas import ProfileSchemaIn, ProfileSchemaOut
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
    profiles = Profile.objects.all().select_related('user')
    # TODO : email in user 
    """
    in pydantic.main.BaseModel.from_orm
    pydantic.error_wrappers.ValidationError: 1 validation error for NinjaResponseSchema
    response -> 0 -> email
    """
    # check if profile is not empty
    if profiles:
        return status.HTTP_200_OK, profiles

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


@profile_controller.post("create_profile",
                         response={200: ProfileSchemaOut, 
                                   404: MessageOut,})
def create_profile(request, profile_in:ProfileSchemaIn):
    # normalize email
    norm_email = profile_in.email.strip().lower().replace(" ", "")
    
    # get the user instance
    try:
        user = User.objects.get(email=norm_email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="User not found.")
    
    skills = [Skill.objects.get_or_create(name=skill.name)[0] 
              for skill in profile_in.skills]

    # create the profile
    profile = Profile.objects.create(
        user=user,
        title=profile_in.title,
        bio=profile_in.bio,
        img=profile_in.img,
    )
    # add many-to-many field skills
    profile.skills.add(*skills)
    profile.save()

    # create response
    project_dict = profile.__dict__
    project_dict["name"] = profile.user.name
    project_dict["email"] = profile.user.email
    project_dict["img"] = str(project_dict["img"])

    profile_out = ProfileSchemaOut(**project_dict)

    return status.HTTP_200_OK, profile_out

