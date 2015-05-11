from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView, CreateView


from project import views as project_views
from accounts import app_settings, forms, models


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


class ProfileView(project_views.BaseTemplateView):
    template_name = 'accounts/profile.html'


class ProfileEditView(project_views.BaseUpdateView):
    template_name = 'accounts/profile_edit.html'
    form_class = forms.ProfileUpdateForm

    def get_success_url(self):
        return reverse('accounts:profile')

    def get_object(self):
        return self.request.user


class PasswordResetFormView(FormView):
    form_class = forms.PasswordResetForm
    template_name = 'accounts/password_reset_form.html'

    def form_valid(self, form):
        opts = {
            'token_generator': default_token_generator,
            'request': self.request,
        }

        form.save(**opts)

        return HttpResponseRedirect(reverse('accounts:password_reset_done'))


class Register(CreateView):
    template_name = 'accounts/register.html'
    form_class = forms.RegistrationForm

    def get_form_kwargs(self):
        kwargs = super(Register, self).get_form_kwargs()
        kwargs['ip_address'] = self.request.META['REMOTE_ADDR']
        return kwargs

    def get_success_url(self):
        return reverse('accounts:registration_complete')

    def render_to_response(self, context, **kwargs):
        if app_settings.REGISTRATION_OPEN:
            return super(Register, self).render_to_response(context, **kwargs)
        return HttpResponseRedirect(reverse('accounts:registration_closed'))


class RegistrationClosed(TemplateView):
    template_name = 'accounts/registration_closed.html'


class RegistrationComplete(TemplateView):
    template_name = 'accounts/registration_complete.html'


class Activate(TemplateView):
    template_name = 'accounts/activate.html'

    def render_to_response(self, context, **kwargs):
        activation_key = self.kwargs['activation_key'].lower()
        account = models.RegistrationProfile.objects.activate_user(activation_key)

        if account is False:
            return super(Activate, self).render_to_response(context, **kwargs)

        return HttpResponseRedirect(reverse('accounts:activation_complete'))


class ActivationComplete(TemplateView):
    template_name = 'accounts/activation_complete.html'
