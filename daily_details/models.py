from django.db import models
from wards.models import Ward


class DailyDetails(models.Model):
    daily_details_date = models.DateField(
        verbose_name="Date",
    )

    daily_details_extra_needs = models.TextField(
        verbose_name="Child's extra needs"
    )

    daily_details_general_mood = models.TextField(
        verbose_name="General Mood"
    )

    daily_details_special_behavior = models.TextField(
        verbose_name="Special Behavior"
    )

    daily_details_meals = models.JSONField(
        verbose_name="Day's Meals",
        default=dict,
        blank=True
    )

    daily_details_naps = models.JSONField(
            verbose_name="Day's Naps",
            default=dict,
            blank=True
    )

    daily_details_meds = models.JSONField(
            verbose_name="Day's Meds",
            default=dict,
            blank=True
    )

    daily_details_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        verbose_name="Ward",
        related_name="daily_details"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["daily_details_ward", "daily_details_date"],
                name="daily_details_ward_date_unique"
            )
        ]