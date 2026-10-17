from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User, Group

# Create your views here.
class AllParentsView(ListView):
    model = User
    template_name = "parents/view_all.html"
    context_object_name = "parents"
    def get_queryset(self):
        parent_group = Group.objects.get(name="Parents")
        return User.objects.filter(groups=parent_group)

class AllStaffView(ListView):
    model = User
    template_name = "staff/view_all.html"
    context_object_name = "staff"
    def get_queryset(self):
        staff_group = Group.objects.get(name="Staff")
        return User.objects.filter(groups=staff_group)

