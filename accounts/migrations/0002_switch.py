# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.contenttypes.models import ContentType
from django.db import migrations


def get_contenttype_id():
    try:
        return ContentType.objects.get(app_label='accounts', model='user').pk
    except ContentType.DoesNotExist:
        return None


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RunSQL([
            "RENAME TABLE auth_user TO accounts_user;"
            "RENAME TABLE auth_user_groups TO accounts_user_groups;",
            "RENAME TABLE auth_user_user_permissions TO accounts_user_user_permissions;"]),
        migrations.RunSQL([
            "DELETE FROM auth_permission WHERE content_type_id={0};".format(get_contenttype_id()),
            "DELETE FROM django_content_type WHERE app_label='accounts' AND model='user'",
            "UPDATE django_content_type SET app_label='accounts' WHERE app_label='auth' AND model='user'"]
        )
    ]
