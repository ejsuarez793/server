# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-17 01:45
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0047_auto_20170117_0135'),
    ]

    operations = [
        migrations.RenameField(
            model_name='movimiento',
            old_name='proveedor',
            new_name='rif_prove',
        ),
    ]
