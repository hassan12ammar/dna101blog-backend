# import libraries
from ninja import Router
from rest_framework import status
from core.authrztion import create_token
from django.contrib.auth import get_user_model
from dna101blog.utlize.validations import normalize_email, password_validator
# import files
from .schemas import SigninIn, SigninUpOut, UserIn, AuthOut, MessageOut
from profile_.models import Profile

User = get_user_model()

auth_controller = Router()

@auth_controller.post("signup", response={
    201: SigninUpOut,
    400: MessageOut,
    })
def signup(request, acount_in: UserIn):
    """
    passwor must contain at least:
    - 8 characters long
    - one letter
    - one digit
    """
    # validadte password
    error_message = password_validator(acount_in.password1)
    if error_message:
        return status.HTTP_400_BAD_REQUEST, {"detail": error_message}
    # check if password1 and password2 are the same
    if acount_in.password1 != acount_in.password2:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="passwords do not match")
    # normalize the data
    email = normalize_email(acount_in.email)
    # check if email is already in use
    if User.objects.filter(email=acount_in.email).exists():
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="Email is already in use")
    # create user
    user = User.objects.create_user(
        # name=name,
        email=email,
        password=acount_in.password1
    )
    # create empty profile with just name and user
    profile = Profile.objects.create(user=user, 
                                     name=acount_in.name)
    # create token for the user
    token = create_token(user)

    return status.HTTP_201_CREATED, SigninUpOut(token=token,
                                                 user=user,
                                                 name=profile.name)


@auth_controller.post("signin", response={
    200: AuthOut,
    404: MessageOut,
    400: MessageOut,
    })
def signin(request, acount_in: SigninIn):
    # normalize email
    email = normalize_email(acount_in.email)
    # check if email exists
    is_user = User.objects.filter(email=email).exists()
    if not is_user:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="User is not registered Or Email is wrong")

    # check if password is correct
    user = User.objects.get(email=email)
    if user.check_password(acount_in.password):
        # create token for user
        token = create_token(user)
        return status.HTTP_200_OK, AuthOut(token=token, user=user)

    return status.HTTP_400_BAD_REQUEST, MessageOut(detail="Wrong password")

