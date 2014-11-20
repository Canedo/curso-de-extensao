# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0014_auto_20141120_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(unique=True, max_length=255, verbose_name=b'Email Principal'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name=b'Bloqueado'),
        ),
    ]
