# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0007_auto_20141111_1036'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monografia',
            name='autor',
            field=models.CharField(default=b'Autor Desconhecido', max_length=255, verbose_name=b'Autor'),
        ),
    ]
