# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import datetime

from django.db import models, migrations
from django.conf import settings
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_changefields'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('activation_key', models.CharField(max_length=40, verbose_name='activation key', editable=False)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL, editable=False)),
                ('created_ip_address', models.GenericIPAddressField(verbose_name='created IP-address', null=True, editable=False, blank=True)),
                ('created', models.DateTimeField(default=datetime.datetime(2015, 5, 11, 19, 3, 37, 528402, tzinfo=utc), verbose_name=b'created', auto_now_add=True)),
            ],
            options={
                'verbose_name': 'registration profile',
                'verbose_name_plural': 'registration profiles',
            },
        ),
    ]
