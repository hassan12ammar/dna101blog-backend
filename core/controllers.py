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
    - one uppercase letter
    - one lowercase letter
    - one digit
    - one special character
    """
    # validadte password
    error_message = password_validator(acount_in.password)
    if error_message:
        return status.HTTP_400_BAD_REQUEST, {"detail": error_message}
    # check if password1 and password2 are the same
    if acount_in.password1 != acount_in.password2:
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="passwords do not match")
    # check if email is already in use
    if User.objects.filter(email=acount_in.email).exists():
        return status.HTTP_400_BAD_REQUEST, MessageOut(detail="Email is already in use")
    # normalize the data
    email = acount_in.email.strip().lower().replace(" ", "")
    name = acount_in.name.strip().lower().title()
    # create user
    self_user = User.objects.create_user(
        name=name,
        email=email,
        password=acount_in.password1
    )

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


@auth_controller.delete("delete_user", response={200: MessageOut, 404: MessageOut})
def delete_user(request, acount_in: SigninIn):
    # get user
    # normalize email 
    email = acount_in.email.strip().lower().replace(" ", "")
    user = User.objects.filter(email=email).first()
    # check if user exists
    if not user:
        return status.HTTP_404_NOT_FOUND, MessageOut(detail="User not found")
    # authenticate user
    signin(request, acount_in)
    # delete user
    user.delete()
    return status.HTTP_200_OK, MessageOut(detail="User deleted successfully")


