# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0020_user_bots'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='enquesta_final_pr13',
            field=models.CharField(default=b'', max_length=1000),
        ),
    ]
