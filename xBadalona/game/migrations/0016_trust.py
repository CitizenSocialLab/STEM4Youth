# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0015_partida_control'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trust',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol', models.CharField(max_length=100)),
                ('seleccio', models.IntegerField(default=-1)),
                ('is_robot', models.BooleanField(default=True)),
                ('rival', models.ForeignKey(related_name='rival_inv1', blank=True, to='game.Trust', null=True)),
                ('user', models.ForeignKey(to='game.User')),
            ],
        ),
    ]
