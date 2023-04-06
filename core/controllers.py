# import libraries
from ninja import Router
from rest_framework import status
from core.authrztion import create_token
from django.contrib.auth import get_user_model
from dna101blog.utlize.validations import password_validator
# import files
from core.schemas import SigninIn, UserIn, AuthOut, MessageOut


User = get_user_model()

auth_controller = Router()

@auth_controller.post("signup", response={
    201: AuthOut,
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
    email = acount_in.email.strip().lower().replace(" ", "")
    # check if email is already in use
    if User.objects.filter(email=acount_in.email).exists():
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="Email is already in use")
    # create user
    self_user = User.objects.create_user(
        # name=name,
        email=email,
        password=acount_in.password1
    )
    # create token for the user
    token = create_token(self_user)
    
    return status.HTTP_201_CREATED, AuthOut(token=token,
                                             user=self_user)


@auth_controller.post("signin", response={
    200: AuthOut,
    404: MessageOut,
    400: MessageOut,
    })
def signin(request, acount_in: SigninIn):
    # check if email exists
    is_user = User.objects.filter(email=acount_in.email).exists()
    if not is_user:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="User is not registered Or Email is wrong")
    # normalize email
    email = acount_in.email.strip().lower().replace(" ", "")
    # check if password is correct
    user = User.objects.get(email=email)
    if user.check_password(acount_in.password):
        # create token for user
        token = create_token(user)
        return status.HTTP_200_OK, AuthOut(token=token, user=user)

    return status.HTTP_400_BAD_REQUEST, MessageOut(detail="Wrong password")

