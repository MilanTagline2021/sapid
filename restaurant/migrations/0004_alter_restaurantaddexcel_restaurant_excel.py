# Generated by Django 3.2.4 on 2021-10-22 06:57

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0003_auto_20211006_0610'),
    ]

    operations = [
        migrations.AlterField(
            model_name='restaurantaddexcel',
            name='restaurant_excel',
            field=models.FileField(upload_to='restaurant-excel', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xlsx', 'xls', 'xlsm', 'csv'])]),
        ),
    ]