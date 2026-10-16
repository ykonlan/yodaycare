from django.contrib import admin
import wards.models as WardModels

# Register your models here.
admin.site.register(WardModels.Ward)
admin.site.register(WardModels.Allergy)
admin.site.register(WardModels.Classroom)