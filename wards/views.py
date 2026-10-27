from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from wards.models import Ward
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from wards.forms import AddWardForm, AllergyFormSet
from django.db import transaction
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

# Create your views here.
class AllWardsView(LoginRequiredMixin, ListView):
    model = Ward
    template_name = "wards/view_all.html"
    context_object_name = "wards"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_ward_form"] = AddWardForm()
        context["ward_allergy_formset"] = AllergyFormSet()
        return context

    def get_queryset(self):
        if self.request.user.groups.filter(name="Administrators").exists():
            return super().get_queryset()
        wards = None
        p_wards = None
        if self.request.user.groups.filter(name="Staff").exists():
            wards = Ward.objects.filter(ward_class=self.request.user.staff_profile.staff_classroom)
        if self.request.user.groups.filter(name="Parents").exists():
            p_wards = Ward.objects.filter(ward_parent__user=self.request.user)
        if (wards is not None) and (p_wards is not None):
            return wards.union(p_wards)
        if wards or p_wards:
            return wards if wards else p_wards
        return Ward.objects.none()


class CreateNewWard(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def post(self, request, *args, **kwargs):
        new_ward_form = AddWardForm(request.POST)
        allergy_formset = AllergyFormSet(request.POST)
        if new_ward_form.is_valid() and allergy_formset.is_valid():
            with transaction.atomic():
                new_ward = new_ward_form.save()
                allergy_formset.instance = new_ward
                allergy_formset.save()
        if new_ward.pk:
            messages.success(request, f"New ward {new_ward.ward_name} saved successfully!")
        return redirect(reverse_lazy("wards-view-all"))

class UpdateWardView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Ward
    fields = ["ward_name", "ward_class", "ward_parent", "ward_dob"]
    template_name = "wards/view_by_id.html"
    context_object_name = "ward"

    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get_success_url(self):
        messages.success(self.request, f"Ward {self.object.ward_name} updated successfully!")
        return reverse_lazy("update-ward", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["ward_form"] = AddWardForm(instance=self.object)
        context["allergies"] = AllergyFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        allergy_formset = AllergyFormSet(self.request.POST, instance=self.object)
        if not allergy_formset.is_valid():
            context = self.get_context_data(form=form)
            context["allergy_formset"] = allergy_formset
            return TemplateResponse(
                self.request,
                self.template_name,
                context
            )
        with transaction.atomic():
            self.object.save()
            allergy_formset.instance = self.object
            allergy_formset.save()

        return HttpResponseRedirect(self.get_success_url())
        
        


            



        



