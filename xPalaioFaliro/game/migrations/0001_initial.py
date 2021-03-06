# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(max_length=300)),
                ('passwd', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Partida',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_partida', models.IntegerField()),
                ('experiment', models.CharField(max_length=100, null=True)),
                ('control_reward', models.CharField(default=b'SOCIAL', max_length=10)),
                ('control_wealth', models.CharField(default=b'EQUAL', max_length=10)),
                ('control_uncertainly', models.IntegerField(default=0)),
                ('always_win', models.BooleanField(default=False)),
                ('num_rondes', models.IntegerField(null=True)),
                ('usuaris_registrats', models.IntegerField(default=0)),
                ('status', models.CharField(default=b'INACTIVA', max_length=20)),
                ('ronda_actual', models.IntegerField(null=True)),
                ('objectiu_aconseguit', models.BooleanField(default=False)),
                ('total_contributed', models.IntegerField(null=True)),
                ('total_social_action', models.IntegerField(null=True)),
                ('data_fi_ronda', models.DateTimeField(null=True)),
                ('date_creation', models.DateTimeField()),
                ('date_start', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
                ('comentari', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pollution',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=10)),
                ('district', models.CharField(max_length=100, null=True)),
                ('school', models.CharField(max_length=100, null=True)),
                ('num_schools', models.IntegerField(null=True)),
                ('NO2', models.FloatField(default=0)),
                ('level', models.CharField(max_length=10, null=True)),
                ('quality', models.CharField(max_length=100, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Ronda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('partida', models.ForeignKey(to='game.Partida')),
                ('num_ronda', models.IntegerField()),
                ('bucket_inici_ronda', models.IntegerField(null=True)),
                ('bucket_final_ronda', models.IntegerField(null=True)),
                ('temps_inici_ronda', models.DateTimeField(null=True)),
                ('temps_final_ronda', models.DateTimeField(null=True)),
                ('calculada', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_robot', models.BooleanField(default=False)),
                ('nickname', models.CharField(default=b'', max_length=100)),
                ('consent', models.BooleanField(default=False)),
                ('status', models.CharField(default=b'', max_length=100)),
                ('pollution', models.ForeignKey(to='game.Pollution', null=True)),
                ('num_jugador', models.IntegerField(null=True)),
                ('partida', models.ForeignKey(to='game.Partida', null=True)),
                ('num_seleccions', models.IntegerField(default=0)),
                ('bots', models.IntegerField(default=0)),
                ('acabat', models.BooleanField(default=False)),
                ('endowment_initial', models.IntegerField(default=0, null=True)),
                ('endowment_current', models.IntegerField(default=0, null=True)),
                ('contributed_public_goods', models.IntegerField(default=0, null=True)),
                ('winnings_public_goods', models.IntegerField(default=0, null=True)),
                ('savings_public_goods', models.IntegerField(default=0, null=True)),
                ('coins_total', models.FloatField(default=0)),
                ('tickets', models.IntegerField(default=0, null=True)),
                ('gender', models.CharField(default=b'', max_length=1)),
                ('age_range', models.CharField(default=b'', max_length=100)),
                ('educational_level', models.CharField(default=b'', max_length=100)),
                ('economic_status', models.CharField(default=b'', max_length=100)),
                ('working_status', models.CharField(default=b'', max_length=100)),
                ('residence', models.CharField(default=b'', max_length=100)),
                ('frame_pr1', models.CharField(default=b'', max_length=100)),
                ('frame_pr2', models.CharField(default=b'', max_length=100)),
                ('frame_pr3', models.CharField(default=b'', max_length=100)),
                ('verification_pr1', models.CharField(default=b'', max_length=100)),
                ('verification_pr2', models.CharField(default=b'', max_length=100)),
                ('verification_pr3', models.CharField(default=b'', max_length=100)),
                ('verification_pr4', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr1', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr2', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr3', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr4', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr5', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr6', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr7', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr8', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr9', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr10', models.CharField(default=b'', max_length=100)),
                ('enquesta_final_pr11', models.CharField(default=b'', max_length=1000)),
                ('date_tutorial', models.DateTimeField(null=True)),
                ('date_register', models.DateTimeField(null=True)),
                ('date_creation', models.DateTimeField(null=True)),
                ('date_end', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRonda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.ForeignKey(to='game.User')),
                ('ronda', models.ForeignKey(to='game.Ronda')),
                ('ha_seleccionat', models.BooleanField(default=False)),
                ('seleccio', models.IntegerField(null=True)),
                ('temps_seleccio', models.DateTimeField(null=True)),
            ],
        ),
    ]
