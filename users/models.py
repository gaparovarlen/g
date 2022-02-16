from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager 
from phonenumber_field.modelfields import PhoneNumberField


class CustomAccountManager(BaseUserManager):
    def create_superuser(self, phone_number, first_name, last_name, password, **other_fields):

        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('superuser must be assigned to is_staff=True.')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('superuser must be assigned to is_superuser=True.')

        return self.create_user(phone_number, first_name, last_name, password, **other_fields)
    
    def create_user(self, phone_number, first_name, last_name, password, **other_fields):

        if not phone_number:
            raise ValueError(_('You must provide a phone_number'))

        user = self.model(phone_number=phone_number, first_name=first_name, last_name=last_name, **other_fields)
        user.set_password(password)
        user.save()
        return user


class NewUser(AbstractBaseUser, PermissionsMixin):
    phone_number = PhoneNumberField(unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    start_date = models.DateTimeField(default=timezone.now)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomAccountManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name
