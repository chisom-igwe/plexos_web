# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-03-22 15:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('plexos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinfo',
            name='Dataset',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='Folder',
        ),
        migrations.RemoveField(
            model_name='userinfo',
            name='Jobset',
        ),
    ]
