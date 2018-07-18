# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_auto_20170322_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diners_dictator',
            field=models.FloatField(default=0),
        ),
    ]
