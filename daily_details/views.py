from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from daily_details.forms import MealFormset, MedFormset, NapFormset, DailyDetailsForm
from wards.models import Ward
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy

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

    def post(self, request, *args, **kwargs):
        ward_id = kwargs["ward_id"]
        ward = Ward.objects.get(id=ward_id)
        nap_form = NapFormset(request.POST, instance=ward)
        meal_form = MealFormset(request.POST, instance=ward)
        med_form = MedFormset(request.POST, instance=ward)
        daily_deets_form = DailyDetailsForm(request.POST, instance=ward)
        if nap_form.is_valid() and meal_form.is_valid() and med_form.is_valid() and daily_deets_form.is_valid():
            daily_deet_id = None
            with transaction.atomic():
                daily_deet = daily_deets_form.save(commit=False)
                daily_deet.daily_details_ward = ward
                daily_deet.daily_details_date = timezone.localdate()
                daily_deet.save()

                med_instances = med_form.save(commit=False)
                for med_instance in med_instances:
                    med_instance.med_date = timezone.localdate()
                    med_instance.med_ward = ward
                    med_instance.save()

                meal_instances = meal_form.save(commit=False)
                for meal_instance in meal_instances:
                    meal_instance.meal_date = timezone.localdate()
                    meal_instance.meal_ward = ward
                    meal_instance.save()

                nap_instances = nap_form.save(commit=False)
                for nap_instance in nap_instances:
                    nap_instance.nap_date = timezone.localdate()
                    nap_instance.nap_ward = ward
                    nap_instance.save()

                print(request.POST)

            if daily_deet.pk:
                messages.success(request, f"Daily Report for {ward.ward_name} filled successfully")
                return redirect(reverse_lazy("add-daily-report", kwargs={"ward_id":ward.id}))

            else:
                messages.error(request, f"Unable to create daily report for {ward.ward_name}")
                return redirect(reverse_lazy("add-daily-report", kwargs={"ward_id":ward.id}))

        else:
            context = {
                "ward" : ward,
                "nap_form" : nap_form,
                "meal_form" : meal_form,
                "med_form" : med_form,
                "daily_deet_form" : daily_deets_form
            }
            return render(request, "daily_details/add.html", context)





            

