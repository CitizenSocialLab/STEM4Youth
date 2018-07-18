# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0003_auto_20160927_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='resultat_joc_inversor1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='resultat_joc_inversor2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='resultat_joc_presoner',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='rival_joc_inversor1',
            field=models.ForeignKey(related_name='rival_inv1', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rival_joc_inversor2',
            field=models.ForeignKey(related_name='rival_inv2', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rival_joc_presoner',
            field=models.ForeignKey(related_name='rival_pres', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='rol_joc_inversor1',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='rol_joc_inversor2',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='seleccio_joc_inversor1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='seleccio_joc_inversor2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='seleccio_joc_presoner',
            field=models.CharField(default=None, max_length=100),
            preserve_default=False,
        ),
    ]
