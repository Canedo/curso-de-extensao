# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0012_auto_20141105_2254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contato',
            name='descricao',
            field=models.CharField(max_length=255, verbose_name=b'Descri\xc3\xa7\xc3\xa3o', blank=True),
        ),
        migrations.AlterField(
            model_name='contato',
            name='tipo',
            field=models.CharField(blank=True, max_length=255, verbose_name=b'Tipo de Contato', choices=[(b'telefone', b'Telefone'), (b'email', b'Email')]),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(max_length=255, unique=True, null=True, verbose_name=b'Email Principal', blank=True),
        ),
    ]
