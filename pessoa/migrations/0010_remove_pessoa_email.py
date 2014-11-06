# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0009_pessoa_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pessoa',
            name='email',
        ),
    ]
