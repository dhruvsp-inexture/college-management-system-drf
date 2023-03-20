from django.db import models


class Course(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.CharField(max_length=500)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    def __str__(self):
        return self.name

