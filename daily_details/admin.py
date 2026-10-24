from django.contrib import admin
from daily_details.models import DailyDetails, Nap, Meal, Med

# Register your models here.
admin.site.register(DailyDetails)
admin.site.register(Nap)
admin.site.register(Med)
admin.site.register(Meal)
