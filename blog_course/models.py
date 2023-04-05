from django.db import models
# 
from profile_.models import Profile

# General model.
class BlogCourse(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    title = models.fields.CharField(max_length=25)
    description = models.fields.CharField(max_length=150)
    content = models.fields.CharField(max_length=2500)

    def __str__(self):
        return f"{self.title} / {self.profile.name}"

# Blog model.
class Blog(BlogCourse):
    img = models.ImageField(upload_to='blog_imgs', null=True, blank=True)

# Course model.
class Course(BlogCourse):
    img = models.ImageField(upload_to='course_imgs', null=True, blank=True)

