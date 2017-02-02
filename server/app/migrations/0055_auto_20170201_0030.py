# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-02-01 00:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0054_auto_20170130_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='factura',
            name='departamento_cc',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name='factura',
            name='f_emi',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='factura',
            name='f_ven',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='factura',
            name='cargo_cc',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='factura',
            name='email_cc',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='factura',
            name='persona_cc',
            field=models.CharField(max_length=100),
        ),
    ]