# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-15 01:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0013_auto_20161115_0113'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='contentpage',
            name='button_target',
        ),
        migrations.RemoveField(
            model_name='contentpage',
            name='button_text',
        ),
    ]