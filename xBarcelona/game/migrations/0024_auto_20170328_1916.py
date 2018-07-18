# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0023_auto_20170328_1136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prisoner',
            name='guess1',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='guess2',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='seleccio1',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='prisoner',
            name='seleccio2',
            field=models.CharField(default=b'', max_length=1),
        ),
    ]
