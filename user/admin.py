from django.contrib import admin
from django.contrib.auth.hashers import make_password
from user.models import Profile

# Register your models here.


class ProfileAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        # Hash the password if it's provided and not already hashed
        if obj.password and not obj.password.startswith('pbkdf2_sha256'):
            obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)


admin.site.register(Profile, ProfileAdmin)
