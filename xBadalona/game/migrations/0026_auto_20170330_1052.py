# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0025_auto_20170330_1008'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='rol1',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='rol2',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
