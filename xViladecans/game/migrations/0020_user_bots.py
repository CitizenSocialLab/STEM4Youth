# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20170508_1248'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bots',
            field=models.IntegerField(default=0),
        ),
    ]
