from django.db import models
# 
from profile_.models import Profile


# model for the course and blog.
class Content(models.Model):
    class TypeChoices(models.TextChoices):
        BLOG = 'BLOG'
        COURSE = 'COURSE'

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

    title = models.fields.CharField(max_length=500)
    description = models.fields.CharField(max_length=150)
    content = models.fields.CharField(max_length=25000)
    img = models.ImageField(upload_to='imgs', null=True, blank=True)
    highlighted = models.BooleanField(default=False)

    content_type = models.CharField(max_length=10, choices=TypeChoices.choices)


    def __str__(self):
        return f"{self.title} / {self.profile.name}"
