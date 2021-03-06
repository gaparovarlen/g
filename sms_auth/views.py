from django.utils.module_loading import import_string

from rest_framework import generics, permissions

from .utils import get_tokens_for_user

from .conf import conf
from .services import AuthService, GeneratorService
from .mixins import ResponsesMixin
from .serializers import \
    AuthSerializer, \
    EntrySerializer, \
    ChangePhoneNumberSerializer
    # DefaultUserSerializer


class EntryAPIView(ResponsesMixin, generics.GenericAPIView):
    """
    Single endpoint to sign-in/sign-up
    :param
        - phone_number
    """

    permission_classes = [
        permissions.AllowAny,
    ]

    serializer_class = EntrySerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            GeneratorService.execute(phone_number=phone_number)
            return self.simple_text_response()
        else:
            return self.error_response(serializer.errors)


class AuthAPIView(ResponsesMixin, generics.GenericAPIView):
    """
    Single endpoint to auth thgrough phone_number + code
        params:
         - phone_number
         - code
    """

    permission_classes = [
        permissions.AllowAny,
    ]

    serializer_class = AuthSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get("phone_number")
            code = serializer.validated_data.get("code")
            user = AuthService.execute(phone_number=phone_number, code=code)
            tokens = get_tokens_for_user(user)

            return self.success_objects_response(tokens)
        else:
            return self.error_response(serializer.errors)