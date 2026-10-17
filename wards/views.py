from django.shortcuts import render
from django.views.generic import ListView
from wards.models import Ward
from users.models import StaffProfile

# Create your views here.
class AllWardsView(ListView):
    model = Ward
    template_name = "wards/view_all.html"
    context_object_name = "wards"

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

