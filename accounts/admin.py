from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from accounts import admin_forms, models


class UserAdmin(DjangoUserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser')
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    form = admin_forms.UserChangeForm
    add_form = admin_forms.UserCreationForm

    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class RegistrationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'activation_key', 'created', 'created_ip_address')
    readonly_fields = ('user', 'activation_key', 'created', 'created_ip_address')
    search_fields = ('user__first_name', 'user__last_name', 'user__email')

    def has_add_permission(self, request):
        return False

admin.site.register(models.User, UserAdmin)
admin.site.register(models.RegistrationProfile, RegistrationProfileAdmin)
