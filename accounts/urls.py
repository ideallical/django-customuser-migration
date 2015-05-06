from django.conf.urls import patterns, url
from django.contrib.auth import views as auth_views

from accounts import views


urlpatterns = patterns(
    '',
    url(r'^login/$', 'django.contrib.auth.views.login',
        {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', views.logout_user, name='logout'),

    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
    url(r'^profile/edit/$', views.ProfileEditView.as_view(), name='profile_edit'),

    url(r'^password/edit/$', auth_views.password_change, name='password_edit', kwargs={'template_name': 'accounts/password_edit.html', 'post_change_redirect': '/profile/'}),

    url(r'^password/reset/$', views.PasswordResetFormView.as_view(), name='password_reset'),
    url(r'^password/reset/done/$', auth_views.password_reset_done, name='password_reset_done', kwargs={'template_name': 'accounts/password_reset_done.html'}),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', auth_views.password_reset_confirm, name='password_reset_confirm', kwargs={'template_name': 'accounts/password_reset_confirm.html', 'post_reset_redirect': '/password/reset/complete/'}),
    url(r'^password/reset/complete/$', auth_views.password_reset_complete, name='password_reset_complete', kwargs={'template_name': 'accounts/password_reset_complete.html'}),

)
