# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-17 01:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_auto_20161115_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='reporte_inicial',
            name='f_vis',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='solicitud',
            name='f_vis',
            field=models.DateField(blank=True, null=True),
        ),
    ]
