# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-01 15:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20170301_1516'),
    ]

    operations = [
        migrations.AddField(
            model_name='presupuesto',
            name='cond_pago',
            field=models.TextField(blank=True, max_length=500),
        ),
        migrations.AddField(
            model_name='presupuesto',
            name='t_ent',
            field=models.TextField(blank=True, max_length=500),
        ),
    ]
