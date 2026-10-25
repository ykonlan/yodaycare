from django import forms
from django.contrib.auth.models import User
from users.models import UserProfile, StaffProfile
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

    def __init__(self, *args, **kwargs):
        editing = kwargs.pop("editing", False)
        super().__init__(*args, **kwargs)
        if editing:
            self.fields.pop("password")

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

class EditStaffProfileForm(forms.ModelForm):
    class Meta:
        model = StaffProfile
        fields = ["staff_classroom"]