from django import forms
from django.contrib.auth.hashers import is_password_usable
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import ugettext_lazy as _

from project.utils import send_template_mail
from accounts import models


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name')


class PasswordResetForm(forms.Form):
    error_messages = {
        'unknown': _("That e-mailaddress doesn't have an associated user account. Are you sure you've registered?"),
        'unusable': _("The user account associated with this e-mailaddress cannot reset the password."),
    }

    email = forms.EmailField(label=_('E-mailaddress'), max_length=254)
    user = None

    def clean_email(self):
        """
        Validates that an active user exists with the given email.
        """
        email = self.cleaned_data['email']
        try:
            self.user = models.User.objects.get(email__iexact=email, is_active=True)
        except models.User.DoesNotExist:
            raise forms.ValidationError(self.error_messages['unknown'])

        if not is_password_usable(self.user.password):
            raise forms.ValidationError(self.error_messages['unusable'])

        return email

    def save(self, token_generator=default_token_generator, request=None):
        extra_context = {
            'uid': urlsafe_base64_encode(str(self.user.id)),
            'user': self.user,
            'token': token_generator.make_token(self.user),
        }

        send_template_mail(
            to_email=self.user.email,
            subject_template='accounts/password_reset_subject.txt',
            email_template='accounts/password_reset_email.html',
            extra_context=extra_context,
            request=request,
        )


class RegistrationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('Password'), widget=forms.PasswordInput)

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'password1')

    def __init__(self, *args, **kwargs):
        self.ip_address = kwargs.pop('ip_address', None)
        return super(RegistrationForm, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        return models.RegistrationProfile.objects.create_inactive_user(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1'],
            created_ip_address=self.ip_address,
        )
