# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-11 14:20
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plexos', '0004_auto_20180409_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='source_file',
            name='url',
            field=models.FileField(upload_to='files\\%H\\%M\\%S', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['xml'])]),
        ),
    ]
