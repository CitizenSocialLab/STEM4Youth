# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0024_auto_20170328_1916'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='diners_premi',
            new_name='diners_prisoner',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='diners_empresari',
            new_name='diners_trust',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_inversor',
        ),
        migrations.RemoveField(
            model_name='user',
            name='diners_punisher',
        ),
        migrations.AddField(
            model_name='dictator',
            name='diners_guanyats1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='dictator',
            name='diners_guanyats2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='diners_guanyats1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='prisoner',
            name='diners_guanyats2',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trust',
            name='diners_guanyats1',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trust',
            name='diners_guanyats2',
            field=models.IntegerField(default=0),
        ),
    ]
