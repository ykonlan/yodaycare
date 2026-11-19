from django.db import models

# Create your models here.
class Holiday(models.Model):
    holiday_name = models.CharField(
        max_length=100,
        verbose_name="Holiday Name"
    )

    holiday_date = models.DateField(
        unique=True
    )
