
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

# additional settings
# we need to be able to create superuser with the new user model (i mean authenticate phone number)
# here i made customuser manager to change createsuper user
# then i have to change command to


class CustomUserManager(BaseUserManager):

    def create_user(self, Phone, password=None, **extra_fields):
        if not Phone:
            raise ValueError('The phone number must be set')
        user = self.model(Phone=Phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, Phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(Phone, password, **extra_fields)
    # Overriding user model


class User(AbstractUser):
    Phone = models.CharField(max_length=11, unique=True, validators=[UnicodeUsernameValidator()])
    USERNAME_FIELD = 'Phone'
    objects = CustomUserManager()
