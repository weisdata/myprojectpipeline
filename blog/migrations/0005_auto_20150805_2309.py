# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='author',
        ),
        migrations.RemoveField(
            model_name='item',
            name='post',
        ),
        migrations.DeleteModel(
            name='Item',
        ),
    ]
