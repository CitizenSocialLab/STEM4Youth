# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20160918_1131'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partida',
            name='diners_heterogenis',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='imatges_refors',
        ),
        migrations.RemoveField(
            model_name='partida',
            name='partida_024',
        ),
    ]
