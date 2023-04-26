# built-in imports
import os
from typing import List
from uuid import uuid4
# third-party imports
from rest_framework import status
from django.contrib.auth import get_user_model
from ninja import Body, File, Router, UploadedFile
# local imports
from .models import Profile, Skill
from core.schemas import MessageOut
from core.authrztion import CustomAuth
from dna101blog.utlize.custom_class import Error
from dna101blog.utlize.validations import get_user_profile, normalize_email
from .schemas import ProfileSchemaIn, ProfileSchemaOut, SkillSchema

# set variables
User = get_user_model()
profile_controller = Router()


@profile_controller.get("get_all_profile", response={200: List[ProfileSchemaOut],},)
def all_profile(request):
    return status.HTTP_200_OK, Profile.objects.all().select_related('user')


@profile_controller.post("create_skill/{skill_name}",
                         response={200: SkillSchema,},
                        auth=CustomAuth(),
                        )
def create_skill(request, skill_name):
    return status.HTTP_200_OK, Skill.objects.get_or_create(name=skill_name)[0]

@profile_controller.get("get_all_skills", response={200: List[SkillSchema],},)
def get_all_skill(request):
    return status.HTTP_200_OK, Skill.objects.all()


@profile_controller.get("get_profile", 
                        response={
                            200: ProfileSchemaOut, 
                            404: MessageOut,
                            400:MessageOut,
                            },
                        auth=CustomAuth(),
                        )
def get_profile(request):
    # get email from auth request
    email = normalize_email(request.auth)

    # check if user and profile exists
    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message

    return status.HTTP_200_OK, profile


@profile_controller.post("create_profile",
                         response={200: ProfileSchemaOut, 
                                   404: MessageOut,
                                   400: MessageOut,
                                   },
                        auth=CustomAuth(),
                        )
def create_profile(request, profile_in:ProfileSchemaIn, img: UploadedFile=None):
    # get email from auth request
    email = normalize_email(request.auth)

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
    )

    # Save profile picture
    if img:
        profile.img.save(f'profile-{profile.id}-{uuid4()}.jpg', img)
    else: profile.img=img

    # add many-to-many field skills
    skills = [Skill.objects.get_or_create(name=skill.name)[0] 
              for skill in profile_in.skills]

    profile.skills.add(*skills)
    # save all changes
    profile.save()

    return status.HTTP_200_OK, profile


@profile_controller.put("edit_profile",
                         response={200: ProfileSchemaOut, 
                                   404: MessageOut,
                                   400: MessageOut,
                                   },
                        auth=CustomAuth(),
                        )
def edit_profile(request, profile_in: ProfileSchemaIn=Body(...), img: UploadedFile=File(None)):
    # get email from auth request
    email = normalize_email(request.auth)

    # Check if user profile exists
    profile = get_user_profile(email)
    if isinstance(profile, Error):
        return profile.status, profile.message

    # Update the user profile
    profile.name = profile_in.name
    profile.title = profile_in.title
    profile.bio = profile_in.bio
    profile.img = profile_in.img

    # Save new profile picture if provided
    if img:
        # remove old img
        if profile.img:
            os.remove(profile.img.path)
        # profile.img = img
        profile.img.save(f'profile-{profile.id}-{uuid4()}.jpg', img)

    # add many-to-many field skills
    skills = [Skill.objects.get_or_create(name=skill.name)[0] 
              for skill in profile_in.skills]
    profile.skills.set(skills)

    # save all changes
    profile.save()

    return status.HTTP_200_OK, profile

