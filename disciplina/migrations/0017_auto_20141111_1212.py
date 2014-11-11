# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('disciplina', '0016_disciplina_turma'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='disciplina',
            options={'verbose_name': 'Disciplina'},
        ),
    ]
