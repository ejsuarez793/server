# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-01-07 04:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0039_reporte_detalle_nombre_t'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte',
            name='tipo',
            field=models.CharField(choices=[('Avance', 'Avance'), ('Problema', 'Problema'), ('Otro', 'Otro')], max_length=10),
        ),
    ]
