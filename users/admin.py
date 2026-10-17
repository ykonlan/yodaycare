from django.contrib import admin
import users.models as UserModels

# Register your models here.
admin.site.register(UserModels.UserProfile)
admin.site.register(UserModels.StaffProfile)
