# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0027_auto_20170330_1253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dictator',
            name='diners_guanyats1',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='dictator',
            name='diners_guanyats2',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='diners_guanyats1',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='diners_guanyats2',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='diners_guanyats3',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trust',
            name='diners_guanyats1',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='trust',
            name='diners_guanyats2',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='user',
            name='diners_prisoner',
            field=models.FloatField(default=0),
        ),
    ]
