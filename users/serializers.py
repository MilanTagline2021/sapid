from django.contrib.auth.hashers import make_password
from django.core.validators import EmailValidator
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from restaurant.models import SaveMenuItem

from users.models import Feedback, User


class UserSerializer(serializers.ModelSerializer):
    save_menu_items = serializers.SerializerMethodField('get_menu_items')

    def get_menu_items(self, instance):
        menu_items = SaveMenuItem.objects.filter(
            user_id=instance.id).order_by('menu_item')
        menuItems = []
        for item in menu_items:
            menuItems.append(item.menu_item.id)
        return menuItems

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email',
                  'provider_type', 'provider_user_id', 'device_id', 'device_type', 'password', 'favourite_restaurants', 'favourite_menu_items', 'save_menu_items')
        extra_kwargs = {
            "device_id": {
                'required': False,
            },
            "device_type": {
                'required': False,
            },
            "password": {
                'required': False,
                'write_only': True,
            },
        }

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            validated_data['password'] = make_password(
                validated_data['password'])
        return super(UserSerializer, self).update(instance, validated_data)


class RegisterUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email',
                  'password', 'device_id', 'device_type')
        extra_kwargs = {
            "email": {
                'required': True,
                'allow_blank': False,
                'validators': [
                    EmailValidator
                ]
            },
            "full_name": {
                'required': True,
                'allow_blank': False,
            },
            "password": {
                'write_only': True
            },
        }

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super(RegisterUserSerializer, self).create(validated_data)


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    default_error_messages = {
        'no_active_account': {'error': {'detail': ['No active account found with the given credentials.']}}
    }

    def validate(self, user_data):
        user_response = super(
            CustomTokenObtainPairSerializer, self).validate(user_data)

        # Access token with to include user detail.
        user_response.pop('refresh')
        user_response.update({
            "user": UserSerializer(self.user).data
        })

        return user_response


class SocialUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'full_name', 'email', 'provider_type',
                  'provider_user_id', 'device_id', 'device_type')
        extra_kwargs = {
            "email": {
                'required': True,
                'allow_blank': False,
                'validators': [
                    EmailValidator
                ]
            },
            "provider_type": {
                'required': True,
                'allow_blank': False,
            },
            "provider_user_id": {
                'required': True,
                'allow_blank': False,
            },
            "password": {'write_only': True},
        }


class GuestUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'device_id', 'device_type', 'provider_type',)


class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = '__all__'


class FcmTokenSerializer(serializers.Serializer):
    DEVICE_TYPE = (
        ('android', 'android'),
        ('ios', 'ios'),
    )
    registration_id = serializers.CharField(max_length=255)
    device_id = serializers.CharField(max_length=255)
    device_type = serializers.ChoiceField(choices=DEVICE_TYPE)
