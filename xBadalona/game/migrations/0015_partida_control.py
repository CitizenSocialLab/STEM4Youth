# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20170309_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='partida',
            name='control',
            field=models.BooleanField(default=True),
        ),
    ]
