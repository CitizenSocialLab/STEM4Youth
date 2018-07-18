# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0011_auto_20161007_1549'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='any_diagnostic',
        ),
        migrations.RemoveField(
            model_name='user',
            name='nucli_convivencia',
        ),
        migrations.RemoveField(
            model_name='user',
            name='prestacio_economica',
        ),
    ]
