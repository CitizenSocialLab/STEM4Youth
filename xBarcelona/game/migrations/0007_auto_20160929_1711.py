# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0006_auto_20160928_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_robot_joc_inversor1',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_robot_joc_inversor2',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='user',
            name='is_robot_joc_premi',
            field=models.BooleanField(default=True),
        ),
    ]
