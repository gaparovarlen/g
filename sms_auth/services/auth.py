from django.contrib.auth import get_user_model

from ..exceptions import SMSCodeNotFoundException, TimeIsExpiredException
from ..conf import conf
from ..models import PhoneCode
from users.models import NewUser
from ..utils import SmsService

User = get_user_model()


class AuthService(SmsService):
    def __init__(self, phone_number: str, code: str):
        self.phone_number = phone_number
        self.code = code

        super().__init__()

    def process(self):
        user = NewUser.objects.\
            filter(phone_number=self.phone_number)\
            .first()
        user.phonecode.code=self.code

        if user is None:
            raise SMSCodeNotFoundException()

        return user
       

