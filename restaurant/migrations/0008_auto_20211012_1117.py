# Generated by Django 3.2.4 on 2021-10-12 11:17

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0007_auto_20211008_0435'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='parent_menu',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='main_menu', to='restaurant.menu'),
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z& ]*$', 'Only alphanumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='city',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z& ]*$', 'Only alphanumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='name',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z& ]*$', 'Only alphanumeric characters are allowed.')]),
        ),
        migrations.AlterField(
            model_name='restaurant',
            name='state',
            field=models.CharField(max_length=255, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z& ]*$', 'Only alphanumeric characters are allowed.')]),
        ),
    ]
