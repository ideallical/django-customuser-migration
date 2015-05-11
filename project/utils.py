import random
from hashlib import md5

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def short_hash(s, use_salt=True):
    if use_salt:
        salt = str(random.random())
        s = salt + s
    return md5(s.encode('utf-8')).hexdigest()[:16]


def send_template_mail(to_email, subject_template, email_template, extra_context, request=None):

    if request:
        use_https = request.is_secure()
    else:
        use_https = False

    context = dict(
        base_url=settings.SITE_SETTINGS['base_url'],
        protocol=use_https and 'https' or 'http',
        site_name=settings.SITE_SETTINGS['name'],
    )

    context.update(extra_context)

    subject = render_to_string(subject_template, context)

    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())
    message = render_to_string(email_template, context)

    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email, ])
