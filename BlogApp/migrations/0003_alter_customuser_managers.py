# Generated by Django 4.2.3 on 2023-07-25 10:19

import django.contrib.auth.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0002_alter_customuser_managers'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='customuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
