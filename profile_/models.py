# libraries import
import uuid
from django.db import models
# local import
from django.contrib.auth import get_user_model

User = get_user_model()

class Skill(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, 
                                related_name='profile_user',
                                null=False, blank=False)
    # more info 
    name = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True, null=True)
    img = models.ImageField(upload_to='profile_imgs', 
                            null=True, blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='profile_skills')

    @property
    def email(self):
        return self.user.email

    def __str__(self):
        return f"{self.name} / {self.user.__str__()}"
