# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-16 06:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0027_auto_20161216_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='presupuesto',
            name='ci_vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='app.Trabajador'),
        ),
    ]