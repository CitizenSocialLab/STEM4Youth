# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0016_trust'),
    ]

    operations = [
        migrations.RenameField(
            model_name='trust',
            old_name='is_robot',
            new_name='is_robot1',
        ),
        migrations.RenameField(
            model_name='trust',
            old_name='rival',
            new_name='rival1',
        ),
        migrations.RenameField(
            model_name='trust',
            old_name='rol',
            new_name='rol1',
        ),
        migrations.RenameField(
            model_name='trust',
            old_name='seleccio',
            new_name='seleccio1',
        ),
        migrations.AddField(
            model_name='trust',
            name='data_seleccio1',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='trust',
            name='data_seleccio2',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='trust',
            name='is_robot2',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='trust',
            name='rival2',
            field=models.ForeignKey(related_name='rival_inv2', blank=True, to='game.Trust', null=True),
        ),
        migrations.AddField(
            model_name='trust',
            name='rol2',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='trust',
            name='seleccio2',
            field=models.IntegerField(default=-1),
        ),
    ]
