# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-20 13:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('studies', '0003_study_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='study',
            options={'permissions': (('view_study', 'View Study'), ('edit_study', 'Edit Study'))},
        ),
    ]