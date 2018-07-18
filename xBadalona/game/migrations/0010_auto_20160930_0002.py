# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0009_user_val_abacus'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='data_seleccio_guess_premi',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_seleccio_inversor1',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_seleccio_inversor2',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='data_seleccio_premi',
            field=models.DateTimeField(null=True),
        ),
    ]
