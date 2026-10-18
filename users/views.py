from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User, Group
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import View

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

class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter("Administrators").exists():
            return reverse_lazy("admin-dashboard")
        if user.groups.filter("Staff").exists():
            return reverse_lazy("staff-dashboard")
        if user.groups.filter("Parents").exists():
            return reverse_lazy("parent-dashboard")
        return super().get_success_url()

class ProfileDashboard(View):
    def get(self, request):
        user = self.request.user
        if user.groups.filter("Administrators").exists():
            return render(request, "staff/admin-dashboard.html")
        elif user.groups.filter("Staff").exists():
            return render(request, "staff/staff-dashboard.html")
        elif user.groups.filter("Parents").exists():
            return render(request, "parents/dashboard.html")



