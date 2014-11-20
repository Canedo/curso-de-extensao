# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0015_auto_20141120_1535'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='bloqueado',
            field=models.BooleanField(default=False, verbose_name=b'Bloqueado'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name=b'Ativo'),
        ),
    ]
