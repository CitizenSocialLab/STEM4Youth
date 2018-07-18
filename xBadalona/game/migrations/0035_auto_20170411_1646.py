# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0034_auto_20170411_1646'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictator',
            name='seleccio1',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='dictator',
            name='seleccio2',
            field=models.FloatField(default=-1),
        ),
        migrations.AlterField(
            model_name='trust',
            name='seleccio1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='trust',
            name='seleccio2',
            field=models.IntegerField(default=-1),
        ),
    ]
