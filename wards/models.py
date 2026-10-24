from django.db import models
from django.core.validators import MinValueValidator
from wards.validators import validator_for_name
from datetime import date

# Create your models here.
class Classroom(models.Model):
    class_population = models.IntegerField(
        default=0,
        editable=False,
        verbose_name="Class Population",
        validators=[MinValueValidator(0)]
    )

    class_name = models.CharField(
        verbose_name="Class Name",
        max_length=100
    )

    def __str__(self):
        return self.class_name


class Ward(models.Model):
    ward_name = models.CharField(
        verbose_name="Ward Name",
        max_length=200,
        validators=[validator_for_name]
    )

    ward_date_added = models.DateField(
        verbose_name="Date Added",
        default=date.today
    )

    ward_parent = models.ForeignKey(
        "users.UserProfile",
        verbose_name="Parent",
        related_name="wards",
        on_delete=models.PROTECT
    )

    ward_class = models.ForeignKey(
        Classroom,
        null=True,
        verbose_name="Ward Class",
        on_delete=models.SET_NULL
    )

    ward_dob = models.DateField(
        verbose_name="Date of birth",
        null=True
    )

    def __str__(self):
        return self.ward_name

class Allergy(models.Model):
    allergy_substance = models.CharField(
        verbose_name="Allergy Substance",
        max_length=500,
    )

    allergy_reaction = models.CharField(
        verbose_name="Expected Allergic Reaction",
        max_length=500,
    )

    allergy_severity_choices = (
        ("high", "High"),
        ("moderate", "Moderate"),
        ("low", "Low")
    )

    allergy_severity = models.CharField(
        verbose_name="Severity of Allergy",
        max_length=10,
        choices=allergy_severity_choices
    )

    allergy_immediate_treatment = models.TextField(
        verbose_name="What to do in case of emergency"
    )

    allergy_ward = models.ForeignKey(
        Ward,
        on_delete=models.CASCADE,
        related_name="allergies"
    )

    def __str__(self):
        return f"{self.allergy_substance} ({self.allergy_ward.ward_name})"
