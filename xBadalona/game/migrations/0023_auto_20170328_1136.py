# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0022_user_diners_punisher'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prisoner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('guess1', models.IntegerField(default=-1)),
                ('seleccio1', models.IntegerField(default=-1)),
                ('is_robot1', models.BooleanField(default=True)),
                ('data_seleccio1', models.DateTimeField(null=True)),
                ('data_guess1', models.DateTimeField(null=True)),
                ('guess2', models.IntegerField(default=-1)),
                ('seleccio2', models.IntegerField(default=-1)),
                ('is_robot2', models.BooleanField(default=True)),
                ('data_seleccio2', models.DateTimeField(null=True)),
                ('data_guess2', models.DateTimeField(null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_guess_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='data_seleccio_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='guess_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_robot_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='rival_joc_premi',
        ),
        migrations.RemoveField(
            model_name='user',
            name='seleccio_joc_premi',
        ),
        migrations.AddField(
            model_name='prisoner',
            name='rival1',
            field=models.ForeignKey(related_name='rival_prisoner1', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='rival2',
            field=models.ForeignKey(related_name='rival_prisoner2', blank=True, to='game.User', null=True),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='user',
            field=models.ForeignKey(to='game.User'),
        ),
    ]
