# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2017-03-01 01:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20170227_2017'),
    ]

    operations = [
        migrations.RenameField(
            model_name='factura',
            old_name='cargo_cc',
            new_name='nro_orden',
        ),
        migrations.RemoveField(
            model_name='factura',
            name='email_cc',
        ),
        migrations.AlterField(
            model_name='factura',
            name='cond_pago',
            field=models.CharField(choices=[('Credito', 'Credito'), ('Contado', 'Contado')], max_length=10),
        ),
    ]
