from datetime import date
from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    start_date = models.DateField(default=date.today())
    end_date = models.DateField(blank=True, null=True)

