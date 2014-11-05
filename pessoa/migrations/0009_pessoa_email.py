# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoa', '0008_auto_20141026_0034'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoa',
            name='email',
            field=models.EmailField(max_length=255, unique=True, null=True, verbose_name=b'email address'),
            preserve_default=True,
        ),
    ]
