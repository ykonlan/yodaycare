from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View, generic
from daily_details.forms import MealFormset, MedFormset, NapFormset, DailyDetailsForm
from wards.models import Ward
from daily_details.models import DailyDetails, Nap, Meal, Med
from django.db import transaction
from django.utils import timezone
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.db import IntegrityError

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
        daily_deet = DailyDetails.objects.filter(daily_details_ward=ward, daily_details_date=timezone.localdate()).first()
        context = {
            "ward" : ward,
            "nap_form" : NapFormset(
                instance=ward,
                queryset=Nap.objects.filter(nap_ward=ward,nap_date=timezone.localdate())
            ),
            "meal_form" : MealFormset(
                instance=ward,
                queryset=Meal.objects.filter(meal_ward=ward,meal_date=timezone.localdate())
            ),
            "med_form" : MedFormset(
                instance=ward,
                queryset=Med.objects.filter(med_ward=ward,med_date=timezone.localdate())
            ),
            "daily_deet_form" : DailyDetailsForm(instance=daily_deet)
        }
        return render(request, "daily_details/add.html", context)

    def post(self, request, *args, **kwargs):
        ward_id = kwargs["ward_id"]
        ward = Ward.objects.get(id=ward_id)
        daily_deet = DailyDetails.objects.filter(daily_details_ward=ward, daily_details_date=timezone.localdate()).first()
        nap_form = NapFormset(request.POST, instance=ward)
        meal_form = MealFormset(request.POST, instance=ward)
        med_form = MedFormset(request.POST, instance=ward)
        daily_deets_form = DailyDetailsForm(request.POST, instance=daily_deet)
        if nap_form.is_valid() and meal_form.is_valid() and med_form.is_valid() and daily_deets_form.is_valid():
            try:
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

            except IntegrityError as e:
                print("Integrity Error:", e)
                messages.error(request, f"Sorry, Daily report for {ward.ward_name} has already been entered for today.")
                return redirect(reverse_lazy("add-daily-report", kwargs={"ward_id":ward.id}))


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

class SeeDailyReportView(LoginRequiredMixin, UserPassesTestMixin, generic.DetailView):
    template_name = "daily_details/view.html"
    context_object_name = "daily_report"

    def test_func(self):
        user = self.request.user
        is_admin = user.groups.filter(name="Administrators").exists()
        if is_admin:
            return True
        ward_id = self.kwargs["pk"]
        ward = Ward.objects.get(id=int(ward_id))
        if user.groups.filter(name="Staff").exists():
            return ward.ward_class == user.staff_profile.staff_classroom
        if user.groups.filter(name="Parents").exists():
            return ward.ward_parent.user == user
        return False

    def get_object(self, queryset = None):
        today = timezone.localdate()
        ward_id = self.kwargs["pk"]
        dd_date = self.request.GET.get("date", today)
        return DailyDetails.objects.filter(daily_details_ward=ward_id, daily_details_date=dd_date).first()

    def get_context_data(self, **kwargs):
        today = timezone.localdate()
        ward_id = self.kwargs["pk"]
        ward = Ward.objects.get(id=ward_id)
        dd_date = self.request.GET.get("date", today)
        context = super().get_context_data(**kwargs)
        context["naps"] = Nap.objects.filter(nap_ward=ward_id, nap_date=dd_date)
        context["meals"] = Meal.objects.filter(meal_ward=ward_id, meal_date=dd_date)
        context["meds"] = Med.objects.filter(med_ward=ward_id, med_date=dd_date)
        context["ward"] = ward
        return context


    





            

