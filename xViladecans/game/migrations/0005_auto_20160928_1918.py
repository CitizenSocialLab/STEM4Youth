# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0004_auto_20160927_1853'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='resultat_joc_presoner',
            new_name='resultat_joc_premi',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='rival_joc_presoner',
            new_name='rival_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='seleccio_joc_presoner',
        ),
        migrations.AddField(
            model_name='user',
            name='seleccio_joc_premi',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='seleccio_joc_inversor1',
            field=models.IntegerField(default=-1),
        ),
        migrations.AlterField(
            model_name='user',
            name='seleccio_joc_inversor2',
            field=models.IntegerField(default=-1),
        ),
    ]
