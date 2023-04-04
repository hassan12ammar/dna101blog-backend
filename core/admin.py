from django.contrib import admin
# from django.contrib.auth import get_user_model
from dna101blog.forms import CustomUserForm
from core.models import CustomUser


class CustomUserAdmin(admin.ModelAdmin):
    # using custom form to validate password
    form = CustomUserForm
    # override default save method to hash password 
    def save_model(self, request, obj, form, change):
        """
        Given a model instance save it to the database.
        """
        obj.set_password(obj.password)
        obj.save()


admin.site.register(CustomUser, CustomUserAdmin)
