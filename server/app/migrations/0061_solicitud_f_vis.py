# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-16 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0060_auto_20170215_1928'),
    ]

    operations = [
        migrations.AddField(
            model_name='solicitud',
            name='f_vis',
            field=models.DateField(null=True),
        ),
    ]
