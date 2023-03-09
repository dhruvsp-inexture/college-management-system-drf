# Generated by Django 4.1.7 on 2023-03-09 06:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('student', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentcoursemapping',
            name='grade',
            field=models.CharField(blank=True, choices=[('A', 'Excellent'), ('B', 'Good'), ('C', 'Satisfactory'), ('D', 'Poor'), ('F', 'Fail')], max_length=1, null=True),
        ),
    ]
