from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, password, is_active=True):
        if not first_name:
            raise ValueError('Users must have a first name')

        if not last_name:
            raise ValueError('Users must have a last name')

        if not email:
            raise ValueError('Users must have an e-mailaddress')

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            email=UserManager.normalize_email(email),
            is_active=is_active,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, email, password):
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class RegistrationManager(models.Manager):

    def activate_user(self, activation_key):
        try:
            profile = self.get(activation_key=activation_key)
        except self.model.DoesNotExist:
            return False
        if not profile.activation_key_expired():
            user = profile.user
            user.is_active = True
            user.save()
            profile.activation_key = 'ALREADY_ACTIVATED'
            profile.save()
            return user

    def create_inactive_user(self, first_name, last_name, email, password, send_email=True, created_ip_address=None):
        User = get_user_model()  # noqa
        new_user = User.objects.create_user(first_name, last_name, email, password, is_active=False)
        registration_profile = self.create_profile(new_user, created_ip_address)

        if send_email:
            send_template_mail(
                to_email=new_user.email,
                subject_template='accounts/activation_email_subject.txt',
                email_template='accounts/activation_email.txt',
                extra_context={
                    'activation_key': registration_profile.activation_key,
                    'expiration_days': app_settings.ACTIVATION_DAYS,
                }
            )

        return new_user

    def create_profile(self, user, created_ip_address=None):
        activation_key = short_hash(user.email, use_salt=True)
        return self.create(user=user, activation_key=activation_key, created_ip_address=created_ip_address)

    def delete_expired_users(self):
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()
