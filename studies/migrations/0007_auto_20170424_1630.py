# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-24 16:30
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import project.fields.datetime_aware_jsonfield


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0011_auto_20170421_2256'),
        ('studies', '0006_study_organization'),
    ]

    operations = [
        migrations.CreateModel(
            name='Response',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('results', project.fields.datetime_aware_jsonfield.DateTimeAwareJSONField(default=dict)),
                ('demographic_snapshot', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='accounts.DemographicData')),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ResponseLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('started', 'Started'), ('paused', 'Paused'), ('abandoned', 'Abandoned'), ('finished', 'Finished')], max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='StudyLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('action', models.CharField(choices=[('created', 'Created'), ('submitted', 'Submitted for Approval'), ('rejected', 'Rejected'), ('approved', 'Approved'), ('started', 'Started'), ('paused', 'Paused'), ('resumed', 'Resumed'), ('deactivated', 'Deactivated'), ('retracted', 'Retracted'), ('viewed_data', 'Viewed Data')], max_length=128)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterField(
            model_name='study',
            name='blocks',
            field=project.fields.datetime_aware_jsonfield.DateTimeAwareJSONField(default=dict),
        ),
        migrations.AddField(
            model_name='response',
            name='study',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='studies.Study'),
        ),
    ]
