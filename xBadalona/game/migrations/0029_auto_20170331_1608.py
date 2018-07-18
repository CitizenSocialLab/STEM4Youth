# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0028_auto_20170330_1653'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='diagnostic',
        ),
        migrations.RemoveField(
            model_name='user',
            name='persona',
        ),
        migrations.AddField(
            model_name='user',
            name='origen',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='pais',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='residencia',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='codi_postal',
            field=models.CharField(default=b'', max_length=6),
        ),
        migrations.AlterField(
            model_name='user',
            name='estat_civil',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='genere',
            field=models.CharField(default=b'', max_length=1),
        ),
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='nivell_estudis',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='rang_edat',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AlterField(
            model_name='user',
            name='situacio_laboral',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
