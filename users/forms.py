from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile
from wards.models import Classroom

class AddUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "first_name",
            "last_name"
        ]
        widgets = {
            "password" : forms.PasswordInput(
                attrs={
                    "placeholder": "Enter Password Here"
                }
            )
        }

        help_texts = {
            "username" : ""
        }

class AddUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "user_phone_1",
            "user_phone_2",
        ]

class StaffProfileForm(forms.Form):
    staff_classroom = forms.ModelChoiceField(
        queryset=Classroom.objects.all()
    )