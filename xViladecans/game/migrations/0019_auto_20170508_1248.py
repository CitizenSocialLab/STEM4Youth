# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0018_user_enquesta_final_pr9'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr10',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr11',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr12',
            field=models.CharField(default=b'', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr13',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
