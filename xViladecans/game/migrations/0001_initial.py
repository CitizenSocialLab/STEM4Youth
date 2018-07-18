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
                ('data_creacio', models.DateTimeField()),
                ('data_inicialitzacio', models.DateTimeField(null=True)),
                ('data_finalitzacio', models.DateTimeField(null=True)),
                ('estat', models.CharField(default=b'INACTIVA', max_length=20)),
                ('classe', models.CharField(max_length=100, null=True)),
                ('num_rondes', models.IntegerField(null=True)),
                ('ronda_actual', models.IntegerField(null=True)),
                ('data_fi_ronda', models.DateTimeField(null=True)),
                ('usuaris_registrats', models.IntegerField(default=0)),
                ('guanyen_igualment', models.BooleanField(default=False)),
                ('diners_heterogenis', models.BooleanField(default=False)),
                ('partida_024', models.BooleanField(default=False)),
                ('comentari', models.CharField(max_length=100, null=True)),
                ('objectiu_aconseguit', models.BooleanField(default=False)),
                ('imatges_refors', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Ronda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('num_ronda', models.IntegerField()),
                ('bucket_inici_ronda', models.IntegerField(null=True)),
                ('bucket_final_ronda', models.IntegerField(null=True)),
                ('temps_inici_ronda', models.DateTimeField(null=True)),
                ('temps_final_ronda', models.DateTimeField(null=True)),
                ('calculada', models.BooleanField(default=False)),
                ('partida', models.ForeignKey(to='game.Partida')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_robot', models.BooleanField(default=False)),
                ('nickname', models.CharField(max_length=100)),
                ('codi_postal', models.CharField(max_length=6)),
                ('genere', models.CharField(max_length=1)),
                ('rang_edat', models.IntegerField()),
                ('nivell_estudis', models.CharField(max_length=100)),
                ('nucli_convivencia', models.CharField(max_length=100)),
                ('prestacio_economica', models.CharField(max_length=100)),
                ('situacio_laboral', models.CharField(max_length=100)),
                ('estat_civil', models.CharField(max_length=100)),
                ('persona', models.CharField(max_length=100)),
                ('check_1', models.CharField(default=b'false', max_length=20)),
                ('num_jugador', models.IntegerField(null=True)),
                ('data_creacio', models.DateTimeField()),
                ('data_finalitzacio', models.DateTimeField(null=True)),
                ('acabat', models.BooleanField(default=False)),
                ('data_registre', models.DateTimeField(null=True)),
                ('diners_inicials', models.IntegerField(null=True)),
                ('diners_actuals', models.IntegerField(null=True)),
                ('num_seleccions', models.IntegerField(default=0)),
                ('guany_final', models.IntegerField(default=0)),
                ('sorteig', models.BooleanField(default=False)),
                ('partida', models.ForeignKey(to='game.Partida', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserRonda',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ha_seleccionat', models.BooleanField(default=False)),
                ('seleccio', models.IntegerField(null=True)),
                ('temps_seleccio', models.DateTimeField(null=True)),
                ('ronda', models.ForeignKey(to='game.Ronda')),
                ('user', models.ForeignKey(to='game.User')),
            ],
        ),
    ]
