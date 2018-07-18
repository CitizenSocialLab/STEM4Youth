# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0031_auto_20170403_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr1',
            new_name='enquesta_final_pr1',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr2',
            new_name='enquesta_final_pr2',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr3',
            new_name='enquesta_final_pr3',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr4',
            new_name='enquesta_final_pr4',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr5',
            new_name='enquesta_final_pr5',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr6',
            new_name='enquesta_final_pr6',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr7',
            new_name='enquesta_final_pr7',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='genere_final_pr8',
            new_name='enquesta_final_pr8',
        ),
        migrations.AddField(
            model_name='user',
            name='enquesta_final_pr9',
            field=models.CharField(default=b'', max_length=100),
        ),
    ]
