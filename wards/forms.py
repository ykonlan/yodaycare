from django import forms
from wards.models import Ward, Allergy
from users.models import UserProfile

class AddWardForm(forms.ModelForm):
    class Meta:
        model = Ward
        fields = ["ward_name", "ward_dob", "ward_parent", "ward_class"]
        widgets = {
            "ward_dob": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["ward_parent"].queryset = UserProfile.objects.filter(user__groups__name="Parents")


class AddWardAllergy(forms.ModelForm):
    class Meta:
        model = Allergy
        fields = ["allergy_substance", "allergy_reaction", "allergy_severity", "allergy_immediate_treatment"]


AllergyFormSet = forms.inlineformset_factory(
    Ward,
    Allergy,
    form=AddWardAllergy,
    fk_name="allergy_ward",
    extra=0,
    can_delete=True
)
