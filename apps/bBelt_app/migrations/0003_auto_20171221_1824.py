# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-21 18:24
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bBelt_app', '0002_trip_trip_join'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trip',
            old_name='pan',
            new_name='plan',
        ),
    ]
