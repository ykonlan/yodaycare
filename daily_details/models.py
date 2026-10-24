from django.db import models
from wards.models import Ward
from django.utils import timezone

class DailyDetails(models.Model):
    daily_details_date = models.DateField(
        verbose_name="Date",
        default=timezone.localdate
    )

    daily_details_extra_needs = models.TextField(
        verbose_name="Child's extra needs",
        null=True
    )

    daily_details_general_mood = models.TextField(
        verbose_name="General Mood"
    )

    daily_details_special_behavior = models.TextField(
        verbose_name="Special Behavior",
        null=True
    )


    daily_details_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        verbose_name="Ward",
        related_name="daily_details"
    )

    def __str__(self):
        return f"{self.daily_details_ward} - {self.daily_details_date}"

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["daily_details_ward", "daily_details_date"],
                name="daily_details_ward_date_unique"
            )
        ]


class Nap(models.Model):
    nap_date = models.DateField(
        default=timezone.localdate,
        verbose_name="Date"
    )

    nap_start_time = models.TimeField(
        verbose_name="Nap Start Time",
    )

    nap_end_time = models.TimeField(
        verbose_name="Nap End Time"
    )

    nap_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        verbose_name="Ward",
        related_name="naps"
    )


class Meal(models.Model):
    meal_name = models.TextField(
        verbose_name="Food"
    )

    meal_amount_choices = (
        ("little", "Little"),
        ("most", "Most"),
        ("all", "All")
    )

    meal_amount_consumed = models.CharField(
        choices=meal_amount_choices,
        verbose_name="Amount Consumed",
        max_length=10
    )

    meal_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        verbose_name="Ward",
        related_name="meals"
    )

    meal_time = models.TimeField(
        verbose_name="Time of meal",
    )

class Med(models.Model):
    med_name = models.TextField(
        verbose_name="Medication",
    )

    med_time = models.TimeField(
        verbose_name="Medication Time",
    )

    med_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        verbose_name="Ward",
        related_name="meds"
    )