# Generated by Django 4.1.7 on 2023-03-03 05:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='end_date',
            field=models.DateField(default=datetime.date(2023, 6, 3)),
        ),
        migrations.AddField(
            model_name='course',
            name='start_date',
            field=models.DateField(default=datetime.date(2023, 3, 3)),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
