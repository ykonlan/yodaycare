from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from daily_details.forms import MealFormset, MedFormset, NapFormset, DailyDetailsForm
from wards.models import Ward

# Create your views here.
class AddDailyReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        is_admin = user.groups.filter(name="Administrators").exists()
        if is_admin:
            return True
        is_staff = user.groups.filter(name="Staff").exists()
        if not is_staff:
            return False
        ward_id = self.kwargs["ward_id"]
        ward = Ward.objects.get(id=int(ward_id))
        ward_class = ward.ward_class
        staff_class = user.staff_profile.staff_classroom
        return ward_class == staff_class
    
    def get(self, request, *args, **kwargs):
        ward = Ward.objects.get(id=int(self.kwargs["ward_id"]))
        context = {
            "ward" : ward,
            "nap_form" : NapFormset(),
            "meal_form" : MealFormset(),
            "med_form" : MedFormset(),
            "daily_deet_form" : DailyDetailsForm()
        }
        return render(request, "daily_details/add.html", context)

