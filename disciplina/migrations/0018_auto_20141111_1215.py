# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disciplina', '0017_auto_20141111_1212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='disciplina',
            name='turma',
            field=models.CharField(max_length=255, verbose_name=b'Turma', blank=True),
        ),
    ]
