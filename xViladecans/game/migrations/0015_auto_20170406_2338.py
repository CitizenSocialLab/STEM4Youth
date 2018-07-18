# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0014_auto_20170309_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='check_1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_guess_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_empresari',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_inversor',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='guess_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_robot_joc_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_robot_joc_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_robot_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rival_joc_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rival_joc_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rival_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rol_joc_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rol_joc_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='seleccio_joc_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='seleccio_joc_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='seleccio_joc_premi',
        ),
    ]
