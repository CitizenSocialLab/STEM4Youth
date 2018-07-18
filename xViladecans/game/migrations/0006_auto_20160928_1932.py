# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0005_auto_20160928_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='guess_joc_premi',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='seleccio_joc_premi',
            field=models.CharField(default=b'', max_length=1),
        ),
    ]
