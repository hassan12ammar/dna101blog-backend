from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

# Overriding the default UserManager for the user model
class EmailAccountManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

    def create_user(self, name,email, password=None, **extra_fields):
        if not email:
            raise ValueError('user must have an email to register')

        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, name, **extra_fields):
        user = self.model(
            email=self.normalize_email(email),
            name=name
        )
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        
        user.save(using=self._db)
        return user

# Overriding the default User model
class CustomUser(AbstractUser, models.Model):
    username = models.NOT_PROVIDED # remove username field
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=100)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    objects = EmailAccountManager()

    # returns the Name and Email of the user 
    def __str__(self):
        return f"{self.name} / {self.email}"

    def natural_key(self):
        return self.email

    class Meta:
        app_label = 'core'
