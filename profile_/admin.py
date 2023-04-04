from django.contrib import admin

from profile_.models import Profile, Skill

# Register models.
admin.site.register(Profile)
admin.site.register(Skill)

"""
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    raw_id_fields = ['user']
"""
