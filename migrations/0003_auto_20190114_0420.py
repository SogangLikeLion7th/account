# Generated by Django 2.1.5 on 2019-01-13 19:20

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20190114_0419'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(verbose_name='Date of Birth'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=account.models.PhoneField(max_length=20, unique=True, verbose_name='Phone Number'),
        ),
    ]