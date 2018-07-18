# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0026_auto_20170330_1052'),
    ]

    operations = [
        migrations.AddField(
            model_name='prisoner',
            name='data_guess3',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='data_seleccio3',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='diners_guanyats3',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='guess3',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='is_robot3',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='rival3',
            field=models.ForeignKey(related_name='rival_prisoner3', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='rol3',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='seleccio3',
            field=models.CharField(default=b'', max_length=1),
        ),
    ]
