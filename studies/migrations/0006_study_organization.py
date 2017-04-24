# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 21:42
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_organization'),
        ('studies', '0005_study_is_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='study',
            name='organization',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='studies', related_query_name='study', to='accounts.Organization'),
            preserve_default=False,
        ),
    ]
