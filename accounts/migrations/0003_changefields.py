# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_switch'),
    ]

    def make_sure_all_users_have_email(self, schema_editor):
        User = self.get_model('accounts', 'User')  # noqa

        for user in User.objects.all():
            if user.email == '':
                user.email = '{username}@example.com'.format(username=user.username)
                user.save()

    operations = [
        migrations.RunPython(make_sure_all_users_have_email),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(unique=True, max_length=254),
        ),
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
