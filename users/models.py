from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        verbose_name="User",
        null=False,
        on_delete=models.CASCADE,
        related_name="profile"
    )

    user_phone_1 = models.CharField(
        verbose_name="User Phone #1",
        max_length=50,
    )

    user_phone_2 = models.CharField(
            verbose_name="User Phone #2",
            max_length=50,
            blank=True
        )

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"    


class StaffProfile(models.Model):
    staff = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Staff",
        related_name="staff_profile",
        null=False
    )

    staff_classroom = models.ForeignKey(
        "wards.Classroom",
        verbose_name="Classroom",
        related_name="staff",
        on_delete=models.PROTECT
    )

    def __str__(self):
        return f"{self.staff.first_name} {self.staff.last_name}"
    
