import datetime
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone

from accounts import app_settings, managers


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)

    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)

    is_staff = models.BooleanField(_('staff status'), default=False,
        help_text=_('Designates whether the user can log into this admin '
                    'site.'))
    is_active = models.BooleanField(_('active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', ]

    objects = managers.UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ('email', )

    def __unicode__(self):
        return self.get_full_name()

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name


class RegistrationProfile(models.Model):
    created = models.DateTimeField('created', editable=False, auto_now_add=True)
    created_ip_address = models.GenericIPAddressField('created IP-address', editable=False, null=True, blank=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, editable=False)
    activation_key = models.CharField(_('activation key'), max_length=40)

    objects = managers.RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')

    def __unicode__(self):
        return 'Registration information for {0}'.format(self.user)

    def activation_key_expired(self):
        expiration_date = datetime.timedelta(days=app_settings.ACTIVATION_DAYS)
        return self.activation_key == 'ALREADY_ACTIVATED' or (self.user.date_joined + expiration_date <= timezone.now())
    activation_key_expired.boolean = True
