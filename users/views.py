from django.shortcuts import render
from django.views.generic import ListView, UpdateView
from django.contrib.auth.models import User, Group
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from users.forms import AddUserForm, AddUserProfileForm, StaffProfileForm, EditStaffProfileForm
from users.models import UserProfile, StaffProfile
from django.db import transaction
from django.shortcuts import redirect
from django.contrib import messages
from django.template.response import TemplateResponse
from django.http import HttpResponseRedirect

# Create your views here.
class AllParentsView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = User
    template_name = "parents/view_all.html"
    context_object_name = "list"

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
    context_object_name = "list"
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
        return user.groups.filter(name="Administrators").exists()

    def post(self, request, *args, **kwargs):
        redirect_page = "dashboard"
        user_type = self.kwargs["user_type"]
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
                        if user_type != "staff":
                            msg = f"New User {request.POST.get('first_name')} {request.POST.get('last_name')} created successfully!"
                            messages.success(request, msg)

                    if user_type == "staff":
                        staff_group = Group.objects.get(name="Staff")
                        new_user.groups.add(staff_group)
                        staff_profile_form = StaffProfileForm(request.POST)
                        if staff_profile_form.is_valid():
                            staff_class = staff_profile_form.cleaned_data["staff_classroom"]
                            new_staff_profile = StaffProfile(staff=new_user, staff_classroom=staff_class)
                            new_staff_profile.save()
                            if new_staff_profile.pk:
                                msg = f"New User {request.POST.get('first_name')} {request.POST.get('last_name')} created successfully!\n{request.POST.get('first_name')} {request.POST.get('last_name')} has been assigned the class {staff_class.class_name}"
                                messages.success(request, msg)
                        redirect_page = "staff-view-all"


                    elif user_type == "parent":
                        parent_group = Group.objects.get(name="Parents")
                        new_user.groups.add(parent_group)
                        redirect_page = "parents-view-all"
            return redirect(redirect_page)
        else:
            return redirect("dashboard")



class UpdateParentView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = "parents/view_by_id.html"
    context_object_name = "parent"

    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get_success_url(self):
        messages.success(self.request, f"Parent {self.object.first_name} {self.object.last_name} updated successfully!")
        return reverse_lazy("update-parent", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["parent_form"] = AddUserForm(instance=self.object, editing=True)
        user_profile = self.object.profile
        context["parent_profile_form"] = AddUserProfileForm(instance=user_profile)
        return context

    def form_valid(self, form):
            user_profile_form = AddUserProfileForm(self.request.POST, instance=self.object.profile)
            if not user_profile_form.is_valid():
                context = self.get_context_data(form=form)
                context["user_profile_form"] = user_profile_form
                return TemplateResponse(
                    self.request,
                    self.template_name,
                    context
                )
            with transaction.atomic():
                self.object.save()
                user_profile_form.save()
    
            return HttpResponseRedirect(self.get_success_url())


class UpdateStaffView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    fields = ["username", "first_name", "last_name", "email"]
    template_name = "staff/view_by_id.html"
    context_object_name = "staff"

    def test_func(self):
        return self.request.user.groups.filter(name="Administrators").exists()

    def get_success_url(self):
        messages.success(self.request, f"Staff {self.object.first_name} {self.object.last_name} updated successfully!")
        return reverse_lazy("update-staff", kwargs={"pk":self.object.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["staff_form"] = AddUserForm(instance=self.object, editing=True)
        user_profile = self.object.profile
        staff_profile = self.object.staff_profile.first()
        context["user_profile_form"] = AddUserProfileForm(instance=user_profile)
        context["staff_profile_form"] = EditStaffProfileForm(instance=staff_profile)
        return context

    def form_valid(self, form):
            user_profile_form = AddUserProfileForm(self.request.POST, instance=self.object.profile)
            staff_profile_form = EditStaffProfileForm(self.request.POST, instance=self.object.staff_profile.first())
            if not user_profile_form.is_valid():
                context = self.get_context_data(form=form)
                context["user_profile_form"] = user_profile_form
                return TemplateResponse(
                    self.request,
                    self.template_name,
                    context
                )

            if not staff_profile_form.is_valid():
                context = self.get_context_data(form=form)
                context["user_profile_form"] = user_profile_form
                context["staff_profile_form"] =  staff_profile_form
                return TemplateResponse(
                    self.request,
                    self.template_name,
                    context
                )

            
            with transaction.atomic():
                self.object.save()
                user_profile_form.save()
                staff_profile_form.save()
    
            return HttpResponseRedirect(self.get_success_url())

    

    
    