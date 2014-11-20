# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0013_auto_20141111_1036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='sobrenome',
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=255, verbose_name=b'Nome Completo'),
        ),
    ]
