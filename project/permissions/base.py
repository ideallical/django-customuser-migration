from __future__ import absolute_import
from django.http import HttpResponseForbidden
from django.template.loader import render_to_string


class Permission(object):
    loggedin_user = None

    def __init__(self, loggedin_user):
        self.loggedin_user = loggedin_user

    def is_authorized(self):
        raise NotImplementedError()

    @property
    def is_admin(self):
        return self.loggedin_user.is_authenticated() and self.loggedin_user.is_super_admin

    @property
    def is_moderator(self):
        return self.loggedin_user.is_authenticated() and self.loggedin_user.is_staff

    @property
    def is_user(self):
        return self.loggedin_user.is_authenticated()

    def response_on_not_authorized(self, context_instance):
        html = render_to_string('403.html', {}, context_instance=context_instance)
        return HttpResponseForbidden(html)


class AdminOnlyPermission(Permission):
    def is_authorized(self):
        return self.is_super_admin


class ModeratorOnlyPermission(Permission):
    def is_authorized(self):
        return self.is_staff


class DefaultPermission(Permission):
    def is_authorized(self):
        return self.is_user


class NoPermissionRequired(Permission):
    def is_authorized(self):
        return True
