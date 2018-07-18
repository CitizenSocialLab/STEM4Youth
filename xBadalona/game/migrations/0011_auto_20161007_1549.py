# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0010_auto_20160930_0002'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='resultat_joc_inversor1',
        ),
        migrations.RemoveField(
            model_name='user',
            name='resultat_joc_inversor2',
        ),
        migrations.RemoveField(
            model_name='user',
            name='resultat_joc_premi',
        ),
    ]
