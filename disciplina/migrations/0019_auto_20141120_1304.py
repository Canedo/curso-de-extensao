# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disciplina', '0018_auto_20141111_1215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='turma',
            field=models.CharField(default=b'', max_length=255, verbose_name=b'Turma', blank=True),
        ),
    ]
