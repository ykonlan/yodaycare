from django.shortcuts import render
from django.views.generic import TemplateView
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from wards.models import Ward, Allergy
from daily_details.models import Nap, Meal, Med

# Create your views here.

class HomePageView(TemplateView):
    template_name = "pages/index.html"

class SeeGeneralReportParentView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        is_daycare_parent = self.request.user.groups.filter(name="Parents").exists()
        ward_id = self.kwargs["pk"]
        ward = Ward.objects.filter(id=ward_id).select_related("ward_parent").first()
        return (is_daycare_parent and (ward.ward_parent.user == self.request.user))

    def get(self, request, *args, **kwargs):
        user = request.user
        if user.groups.filter(name="Parents").exists():
            ward = Ward.objects.filter(id=kwargs["pk"]).first()
            allergies = Allergy.objects.filter(allergy_ward=ward)
            naps = Nap.objects.filter(nap_ward=ward)
            meds = Nap.objects.filter(med_ward=ward)
            meals = Allergy.objects.filter(meal_ward=ward)
            context = {
                "ward" : ward,
                "allergies" : allergies,
                "naps" : naps,
                "meds" : meds,
                "meals" : meals
            }
            return render(request, "parents/general_report.html", context)

class SeeGeneralReportStaffView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Staff").exists()

    def get(self, request, *args, **kwargs):
        context = {

        }
        return render(request, "staff/general_report_staff.html", context)


class SeeGeneralReportAdminView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get(self, request, *args, **kwargs):
        context = {
            
        }
        return render(request, "staff/general_report_admin.html", context)
    


