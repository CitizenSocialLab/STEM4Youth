# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0017_auto_20170322_1134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trust',
            name='rival1',
            field=models.ForeignKey(related_name='rival1', blank=True, to='game.User', null=True),
        ),
        migrations.AlterField(
            model_name='trust',
            name='rival2',
            field=models.ForeignKey(related_name='rival2', blank=True, to='game.User', null=True),
        ),
    ]
