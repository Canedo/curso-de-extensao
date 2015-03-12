# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import downloads.models


class Migration(migrations.Migration):

    dependencies = [
        ('downloads', '0008_auto_20141120_1304'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monografia',
            name='arquivo',
            field=downloads.models.NewFileField(null=True, upload_to=b'', blank=True),
        ),
    ]
