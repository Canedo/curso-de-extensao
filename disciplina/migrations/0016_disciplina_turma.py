# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disciplina', '0015_auto_20141111_1036'),
    ]

    operations = [
        migrations.AddField(
            model_name='disciplina',
            name='turma',
            field=models.CharField(default='EL1', max_length=255, verbose_name=b'Turma'),
            preserve_default=False,
        ),
    ]
