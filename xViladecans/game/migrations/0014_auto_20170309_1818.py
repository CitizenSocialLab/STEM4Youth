# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0013_remove_user_sorteig'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='rang_edat',
            field=models.CharField(max_length=20),
        ),
    ]
