# import libraries
from typing import List
from ninja import Router
from rest_framework import status
from django.contrib.auth import get_user_model
# import files
# import models
from profile_.models import Profile, Skill
# import schemas
from core.schemas import MessageOut #, UserOut
from profile_.schemas import ProfileSchemaIn, ProfileSchemaOut, SkillSchema
# import functions
from dna101blog.utlize.validations import get_user_profile
# import custom classes
from core.authrztion import CustomAuth
from dna101blog.utlize.custom_class import Error

# set variables
User = get_user_model()
profile_controller = Router()

"""
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
    # check if profile is not empty
    if profiles:
        return status.HTTP_200_OK, profiles

    return status.HTTP_404_NOT_FOUND, MessageOut(detail="No profile found")
"""


@profile_controller.post("create_skill/{name}",
                         response={200: SkillSchema,},
                        auth=CustomAuth(),
                        )
def create_skill(request, skill_name):
    return Skill.objects.get_or_create(name=skill_name)[0]


@profile_controller.get("get_profile", 
                        response={
                            200: ProfileSchemaOut, 
                            404: MessageOut,
                            400:MessageOut,
                            },
                        auth=CustomAuth(),
                        )
def get_profile(request):
    # normailze email
    email = request.auth

    # check if user and profile exists
    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message

    return status.HTTP_200_OK, profile


@profile_controller.post("create_profile",
                         response={200: ProfileSchemaOut, 
                                   404: MessageOut,
                                   },
                        auth=CustomAuth(),
                        )
def create_profile(request, profile_in:ProfileSchemaIn):
    # normalize email
    email = request.auth

    # get the user instance
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="User not found.")

    profile_exists = Profile.objects.filter(user=user).exists()
    if profile_exists:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="Profile alrady exists.")

    # create the profile
    profile = Profile.objects.create(
        user=user,
        name=profile_in.name,
        title=profile_in.title,
        bio=profile_in.bio,
        img=profile_in.img,
    )
    # add many-to-many field skills
    skills = [Skill.objects.get_or_create(name=skill.name)[0] 
              for skill in profile_in.skills]

    profile.skills.add(*skills)
    profile.save()

    # create response
    project_dict = profile.__dict__
    # project_dict["name"] = profile.name
    project_dict["email"] = profile.user.email
    project_dict["img"] = str(project_dict["img"])

    profile_out = ProfileSchemaOut(**project_dict)

    return status.HTTP_200_OK, profile_out


@profile_controller.put("edit_profile",
                         response={200: ProfileSchemaOut, 
                                   404: MessageOut,
                                   },
                         auth=CustomAuth(),
                         )
def edit_profile(request, profile_in: ProfileSchemaIn):
    # Get the user's email
    email = request.auth

    # Check if user profile exists
    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message

    # Update the user profile
    profile.name = profile_in.name
    profile.title = profile_in.title
    profile.bio = profile_in.bio
    profile.img = profile_in.img

    # add many-to-many field skills
    skills = [Skill.objects.get_or_create(name=skill.name)[0] 
              for skill in profile_in.skills]

    profile.skills.set(skills)
    profile.save()

    return status.HTTP_200_OK, profile


