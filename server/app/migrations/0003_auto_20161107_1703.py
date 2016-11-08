# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-07 17:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('app', '0002_auto_20161102_2351'),
    ]

    operations = [
        migrations.AddField(
            model_name='trabajador',
            name='usuario',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='correo',
            field=models.EmailField(max_length=254),
        ),
        migrations.AlterField(
            model_name='trabajador',
            name='dire',
            field=models.CharField(blank=True, max_length=50),
        ),
    ]
