# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0006_auto_20141026_0034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='arquivohistorico',
            options={'verbose_name': 'Estat\xedsticas de Download', 'verbose_name_plural': 'Estat\xedsticas de Download'},
        ),
        migrations.AlterModelOptions(
            name='monografia',
            options={'verbose_name': 'Monografia'},
        ),
        migrations.AddField(
            model_name='monografia',
            name='autor',
            field=models.CharField(default='Igor', max_length=255, verbose_name=b'Autor'),
            preserve_default=False,
        ),
    ]
