# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0021_user_diners_dictator'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='diners_punisher',
            field=models.FloatField(default=0),
        ),
    ]
