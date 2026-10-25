from django.forms import ModelForm
from daily_details.models import DailyDetails, Nap, Meal, Med
from wards.models import Ward
from django.forms import inlineformset_factory

class DailyDetailsForm(ModelForm):
    class Meta:
        model = DailyDetails
        fields = ["daily_details_extra_needs", "daily_details_general_mood", "daily_details_special_behavior" ]

class NapForm(ModelForm):
    class Meta:
        model = Nap
        fields = ["nap_start_time", "nap_end_time"]

class MealForm(ModelForm):
    class Meta:
        model = Meal
        fields = ["meal_name", "meal_time", "meal_amount_consumed"]

class MedForm(ModelForm):
    class Meta:
        model = Med
        fields = ["med_name", "med_time"]

NapFormset = inlineformset_factory(
    Ward,
    Nap,
    form=NapForm,
    fk_name="nap_ward",
    extra=1,
    can_delete=True
)

MealFormset = inlineformset_factory(
    Ward,
    Meal,
    form=MealForm,
    fk_name="meal_ward",
    extra=1,
    can_delete=True
)

MedFormset = inlineformset_factory(
    Ward,
    Med,
    form=MedForm,
    fk_name="med_ward",
    extra=1,
    can_delete=True
)

