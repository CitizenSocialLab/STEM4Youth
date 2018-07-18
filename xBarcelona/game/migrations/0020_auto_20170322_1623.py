# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0019_auto_20170322_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Dictator',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rol1', models.CharField(max_length=100)),
                ('seleccio1', models.IntegerField(default=-1)),
                ('is_robot1', models.BooleanField(default=True)),
                ('data_seleccio1', models.DateTimeField(null=True)),
                ('rol2', models.CharField(max_length=100)),
                ('seleccio2', models.IntegerField(default=-1)),
                ('is_robot2', models.BooleanField(default=True)),
                ('data_seleccio2', models.DateTimeField(null=True)),
                ('rival1', models.ForeignKey(related_name='rival_dictator1', blank=True, to='game.User', null=True)),
                ('rival2', models.ForeignKey(related_name='rival_dictator2', blank=True, to='game.User', null=True)),
                ('user', models.ForeignKey(to='game.User')),
            ],
        ),
        migrations.AlterField(
            model_name='trust',
            name='rival1',
            field=models.ForeignKey(related_name='rival_trust1', blank=True, to='game.User', null=True),
        ),
        migrations.AlterField(
            model_name='trust',
            name='rival2',
            field=models.ForeignKey(related_name='rival_trust2', blank=True, to='game.User', null=True),
        ),
    ]
