from django.contrib.auth.tokens import default_token_generator
from django.core.urlresolvers import reverse
from django.contrib.auth.views import logout
from django.http import HttpResponseRedirect
from django.views.generic import FormView

from project import views as project_views
from accounts import forms


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
