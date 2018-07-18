# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0033_auto_20170406_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trust',
            name='seleccio1',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='trust',
            name='seleccio2',
            field=models.FloatField(default=-1),
        ),
    ]
