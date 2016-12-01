# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-01 19:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='system_name',
            field=models.CharField(help_text='Internally used name', max_length=100, unique=True),
        ),
    ]
