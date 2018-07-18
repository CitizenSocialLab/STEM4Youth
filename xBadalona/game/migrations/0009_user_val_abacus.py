# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0008_auto_20160929_2312'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='val_abacus',
            field=models.IntegerField(default=0),
        ),
    ]
