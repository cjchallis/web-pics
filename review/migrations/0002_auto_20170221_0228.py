# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='picfile',
            name='path',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='picfile',
            name='status',
            field=models.TextField(default=''),
        ),
    ]
