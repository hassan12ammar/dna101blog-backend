# import libraries
from django.db import models
import uuid
# import my files
from django.contrib.auth import get_user_model

User = get_user_model()

class Skill(models.Model):
    name = models.CharField(max_length=25)
    
    def __str__(self) -> str:
        return self.name


class Profile(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, 
                                related_name='profile_user', editable=False, 
                                null=False, blank=False)
    # more info 
    title = models.CharField(max_length=50)
    bio = models.TextField(max_length=500, blank=True)
    img = models.ImageField(upload_to='profile_imgs', blank=True)
    skills = models.ManyToManyField(Skill, blank=True, related_name='profile_skills')


    def __str__(self):
        return self.user.__str__()
