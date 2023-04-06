from django.contrib import admin

from profile_.models import Profile, Skill

# Register models.
admin.site.register(Profile)
admin.site.register(Skill)
