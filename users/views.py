from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User, Group
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from users.forms import AddUserForm, AddUserProfileForm, StaffProfileForm
from users.models import UserProfile, StaffProfile
from django.db import transaction
from django.shortcuts import redirect

# Create your views here.
class AllParentsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "parents/view_all.html"
    context_object_name = "parents"

    def test_func(self):
        user = self.request.user
        return user.groups.filter(name="Administrators").exists()

    def get_queryset(self):
        parent_group = Group.objects.get(name="Parents")
        return User.objects.filter(groups=parent_group)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_user_form"] = AddUserForm()
        context["new_user_profile_form"] = AddUserProfileForm()
        return context


class AllStaffView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "staff/view_all.html"
    context_object_name = "staff"
    def get_queryset(self):
        staff_group = Group.objects.get(name="Staff")
        return User.objects.filter(groups=staff_group)

    def test_func(self):
            user = self.request.user
            return user.groups.filter(name="Administrators").exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["new_user_form"] = AddUserForm()
        context["new_user_profile_form"] = AddUserProfileForm()
        context["new_staff_form"] = StaffProfileForm()
        return context

    


class CustomLoginView(auth_views.LoginView):
    def get_success_url(self):
        return reverse_lazy("dashboard")

class ProfileDashboard(View):
    def get(self, request):
        user = self.request.user
        if user.groups.filter(name="Administrators").exists():
            return render(request, "staff/admin-dashboard.html")
        elif user.groups.filter(name="Staff").exists():
            return render(request, "staff/staff-dashboard.html")
        elif user.groups.filter(name="Parents").exists():
            return render(request, "parents/dashboard.html")

class CreateUserView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        user = self.request.user
        return user.groups.filter(groups__name="Administrators").exists()

    def post(self, request, *args, **kwargs):
        user_type = args[0]
        msg = None
        user_form = AddUserForm(request.POST)
        user_profile_form = AddUserProfileForm(request.POST)
        if user_type in ("parent", "administrator", "staff"):
            if user_form.is_valid() and user_profile_form.is_valid():
                with transaction.atomic():
                    new_user = user_form.save(commit=False)
                    new_user.set_password(request.POST.get("password"))
                    new_user.save()

                    new_user_profile = UserProfile(
                        user = new_user,
                        user_phone_1 = request.POST.get("user_phone_1"),
                        user_phone_2 = request.POST.get("user_phone_2")
                    )
                    new_user_profile.save()
                    if new_user_profile.pk:
                        msg = f"New User {request.POST.get('first_name')} {request.POST.get('last_name')} created successfully!"

                    if user_type == "staff":
                        staff_profile_form = StaffProfileForm(request.POST)
                        if staff_profile_form.is_valid():
                            staff_class = staff_profile_form.cleaned_data["staff_classroom"]
                            new_staff_profile = StaffProfile(user=new_user, staff_classroom=staff_class)
                            new_staff_profile.save()
                            if new_staff_profile.pk:
                                msg = "\n".join([msg, f"{request.POST.get('first_name')} {request.POST.get('last_name')} has been assigned the class {staff_class.class_name}"])
            return render(request, "admin/create-new-user.html", {"user_form": user_form, "user_profile_form": user_profile_form, "msg":msg})
        else:
            return redirect("dashboard")

                    




            





