import code
from ..exceptions import \
    SMSWaitException, \
    UserDoesntExistException

from ..models import PhoneCode
from users.models import NewUser
from ..utils import SmsService
from ..conf import conf
from ..utils import send_sms, random_code, valid_to
from django.core.exceptions import ObjectDoesNotExist



class GeneratorService(SmsService):
    def __init__(self, phone_number: str):
        self.phone_number = phone_number

    def process(self):
        if self.phone_number is not None:
            user = NewUser.objects\
                .filter(phone_number=self.phone_number)\
                .first()

        if user is None:
            raise UserDoesntExistException()



        try :
            phone = PhoneCode.objects.get(owner=user)
            if not phone.is_allow:
                raise SMSWaitException()
            phone.code=random_code()
            phone.valid_to=valid_to()
            send_sms(phone.code, user.phone_number)
            phone.save()
        except ObjectDoesNotExist:
            code=random_code()
            valid=valid_to()
            r = PhoneCode(owner=user, code=code, valid_to=valid)
            r.save()
            print('here')
            

