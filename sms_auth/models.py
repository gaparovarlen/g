from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from .utils import random_code, valid_to
from users.models import NewUser


class SMSMessage(models.Model):
    """
    Save sended sms after as history
    """

    created = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField("Phone number", max_length=20)

    def __str__(self):
        return f"{self.phone_number} / {self.created}"

    def __repr__(self):
        return f"{self.phone_number}"

    class Meta:
        verbose_name = "Sms log"
        verbose_name_plural = "Sms log"


class PhoneCode(models.Model):
    """
    After validation save phone code instance
    """

    owner = models.OneToOneField(get_user_model(),
                              null=True,
                              on_delete=models.CASCADE)
    code = models.PositiveIntegerField(blank=True, null=True)
    valid_to = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("created_at",)
        verbose_name = "Phone code"
        verbose_name_plural = "Phone codes"

    def __str__(self):
        return f"{self.owner} ({self.code})"

    def __repr__(self):
        return self.__str__()

    @property
    def is_allow(self):
        return timezone.now() >= self.valid_to

    @property
    def message(self) -> str:
        return f"Your auth code: {self.code}"

