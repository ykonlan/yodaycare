from django.shortcuts import render
from django.views.generic import ListView
from wards.models import Ward
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from wards.forms import AddWardForm, AddWardAllergy

# Create your views here.
class AllWardsView(ListView):
    model = Ward
    template_name = "wards/view_all.html"
    context_object_name = "wards"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_ward_form"] = AddWardForm()
        context["ward_allergy_form"] = AddWardAllergy()
        return context

    def get_queryset(self):
        if self.request.user.groups.filter(name="Administrators").exists():
            return super().get_queryset()
        wards = None
        p_wards = None
        if self.request.user.groups.filter(name="Staff").exists():
            wards = Ward.objects.filter(ward_class=self.request.user.staff_profile.first().staff_classroom)
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
        new_ward_form = AddWardForm()



        



