# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-06 09:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0037_auto_20170106_0718'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='etapa',
            unique_together=set([('codigo_pro', 'letra')]),
        ),
    ]