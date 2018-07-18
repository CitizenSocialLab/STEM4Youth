# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0029_auto_20170331_1608'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='check_1',
        ),
    ]
