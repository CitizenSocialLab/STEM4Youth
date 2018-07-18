# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0032_auto_20170406_1509'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='val_abacus',
            new_name='vals',
        ),
    ]
