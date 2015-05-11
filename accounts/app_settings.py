from django.conf import settings


REGISTRATION_OPEN = getattr(settings, 'ACCOUNTS_REGISTRATION_OPEN', False)
ACTIVATION_DAYS = getattr(settings, 'ACCOUNT_ACTIVATION_DAYS', 7)
