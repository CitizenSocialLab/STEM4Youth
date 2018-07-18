# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0007_auto_20160929_1711'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diners_clima',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='diners_empresari',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='diners_inversor',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='diners_premi',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='diners_total',
            field=models.FloatField(default=0),
        ),
    ]
