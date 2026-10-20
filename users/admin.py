from django.contrib import admin
import users.models as UserModels

# Register your models here.
admin.site.register(UserModels.UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "user_phone_1",
        "user_phone_2",
    ]

admin.site.register(UserModels.StaffProfile)
