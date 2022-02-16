import random
from abc import ABC, abstractmethod
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

import os
from twilio.rest import Client
from rest_framework_simplejwt.tokens import RefreshToken


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class SmsService(ABC):
    @classmethod
    def execute(cls, **kwargs):
        instance = cls(**kwargs)
        with transaction.atomic():
            return instance.process()

    @abstractmethod
    def process(self):
        pass


def valid_to():
    from .conf import conf

    now = timezone.now()
    delta = conf.SMS_TIMELIFE
    due_at = now + timedelta(seconds=delta)

    return due_at


def random_n(n) -> int:
    range_start = 10 ** (n - 1)
    range_finish = (10 ** n) - 1

    return random.randint(range_start, range_finish)


def random_code() -> int:
    from .conf import conf

    code = random_n(conf.SMS_AUTH_CODE_LEN)

    return code


account_sid = 'AC0fc3010b554ee6f8a328e0db09485fea'
auth_token = 'b09f49b6950a77dc328291e12a62a44d'
client = Client(account_sid, auth_token)

def send_sms(user_code, phone_number):
    message = client.messages.create(
                                body=f'И этот код тоже отправь {user_code}',
                                from_='+17755227937',
                                to=f'{phone_number}'
                            )

    print(message.sid)
