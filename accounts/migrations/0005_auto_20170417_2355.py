# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-17 23:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20170413_2024'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participantprofile',
            name='age',
            field=models.CharField(choices=[('<18', 'under 18'), ('18-21', '18-21'), ('22-24', '22-24'), ('25-29', '25-29'), ('30-34', '30-34'), ('35-39', '35-39'), ('40-44', '40-44'), ('45-59', '45-49'), ('50s', '50-59'), ('60s', '60-69'), ('>70', '70 or over')], max_length=5),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='annual_income',
            field=models.CharField(choices=[('0', '0'), ('5000', '5000'), ('10000', '10000'), ('15000', '15000'), ('20000', '20000'), ('30000', '30000'), ('40000', '40000'), ('50000', '50000'), ('60000', '60000'), ('70000', '70000'), ('80000', '80000'), ('90000', '90000'), ('100000', '100000'), ('110000', '110000'), ('120000', '120000'), ('130000', '130000'), ('140000', '140000'), ('150000', '150000'), ('160000', '160000'), ('170000', '170000'), ('180000', '180000'), ('190000', '190000'), ('>200000', 'over 200000'), ('na', 'prefer not to answer')], max_length=7),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='density',
            field=models.CharField(choices=[('urban', 'urban'), ('suburban', 'suburban'), ('rural', 'rural')], max_length=8),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='education_level',
            field=models.CharField(choices=[('some', 'some or attending high school'), ('hs', 'high school diploma or GED'), ('col', 'some or attending college'), ('assoc', '2-year college degree'), ('bach', '4-year college degree'), ('grad', 'some or attending graduate or professional school'), ('prof', 'graduate or professional degree')], max_length=5),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='gender',
            field=models.CharField(choices=[('m', 'male'), ('f', 'female'), ('o', 'other'), ('na', 'prefer not to answer')], max_length=2),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='number_of_children',
            field=models.CharField(choices=[('0', '0'), ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10'), ('>10', 'More than 10')], max_length=3),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='number_of_guardians',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3>', '3 or more'), ('varies', 'varies')], max_length=6),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='race_identification',
            field=models.CharField(choices=[('white', 'White'), ('hisp', 'Hispanic, Latino, or Spanish origin'), ('black', 'Black or African American'), ('asian', 'Asian'), ('native', 'American Indian or Alaska Native'), ('mideast-naf', 'Middle Eastern or North African'), ('hawaiian-pac-isl', 'Native Hawaiian or Other Pacific Islander'), ('other', 'Another race, ethnicity, or origin')], max_length=16),
        ),
        migrations.AlterField(
            model_name='participantprofile',
            name='spouse_education_level',
            field=models.CharField(choices=[('some', 'some or attending high school'), ('hs', 'high school diploma or GED'), ('col', 'some or attending college'), ('assoc', '2-year college degree'), ('bach', '4-year college degree'), ('grad', 'some or attending graduate or professional school'), ('prof', 'graduate or professional degree'), ('na', 'not applicable - no spouse or partner')], max_length=5),
        ),
    ]