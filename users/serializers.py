from rest_framework import serializers
from users.models import NewUser


class RegisterUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = NewUser
        fields = ['phone_number', 'first_name', 'last_name']
