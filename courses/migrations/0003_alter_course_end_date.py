# Generated by Django 4.1.7 on 2023-03-03 10:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0002_course_end_date_course_start_date_alter_course_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
