# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20170421_1423'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr9',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
