from django.contrib.auth.models import BaseUserManager
from django.contrib.gis.db.models import GeoManager


class UserManager(BaseUserManager, GeoManager):

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
