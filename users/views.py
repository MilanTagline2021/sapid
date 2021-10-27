from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.db.models import Q
from push_notifications.models import APNSDevice, GCMDevice
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User

from .serializers import *


def user_access_token(user, context, is_created=False):
    refresh = RefreshToken.for_user(user)
    response = {
        "access": str(refresh.access_token),
        "user": UserSerializer(user, context=context).data,
    }
    if is_created:
        response['message'] = "User created successfully."

    return Response(response)


class CutomObtainPairView(TokenObtainPairView):
    """ Create API view for serializer class 'CustomTokenObtainPairSerializer' """
    serializer_class = CustomTokenObtainPairSerializer


class RegisterUserView(generics.GenericAPIView):
    """ Create API view for serializer class "RegisterUserSerializer" and "UserSerializer".
    This view verify all input and create new user """
    serializer_class = RegisterUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        if User.objects.filter(email__iexact=request.data['email']).exists():
            return Response({'error': {"email": ["Your email already register. please login with password."]}}, status=400)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)


class SocialUserView(generics.GenericAPIView):
    serializer_class = SocialUserSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        get_user = User.objects.filter(
            Q(email__iexact=request.data['email']) | (Q(email__isnull=True) & ~Q(provider_type='guest') & Q(device_id=request.data['device_id'])))

        if get_user.exists():
            get_user.update(**serializer.data)
            return user_access_token(get_user.first(), self.get_serializer_context(), is_created=False)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)


class GuestUserView(generics.GenericAPIView):
    serializer_class = GuestUserSerializer

    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        get_user = User.objects.filter(
            device_id__iexact=request.data['device_id'], provider_type='guest')

        if get_user.exists():
            return user_access_token(get_user.first(), self.get_serializer_context(), is_created=False)

        user = serializer.save()
        return user_access_token(user, self.get_serializer_context(), is_created=True)


class UserUpdateView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request, format=None):
        user = self.request.user
        serializer = UserSerializer(user, data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        get_user = User.objects.filter(id=user.id,
                                       provider_type='guest')
        if get_user.exists():
            return Response({'error': {"message": ["This user is guest user..!!"]}}, status=403)

        serializer.save()
        return Response(serializer.data)

    def delete(self, request, format=None):
        user_id = self.request.user.id
        User.objects.filter(id=user_id).delete()
        return Response({"message": [f"User {user_id} deleted successfully..!!"]}, status=204)


class FeedbackAPI(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FeedbackSerializer

    def post(self, request, format=None):
        if request.data:
            _mutable = request.data._mutable
            request.data._mutable = True
            request.data['user'] = request.user.id
            request.data._mutable = _mutable

        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)

        serializer.save()
        return Response(serializer.data)


class FcmTokenAPI(generics.CreateAPIView):
    serializer_class = FcmTokenSerializer

    def post(self, request, format=None):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response({'error': serializer.errors}, status=400)
        fcm_data = serializer.data
        user = self.request.user

        defaults = {
            'registration_id': fcm_data['registration_id']
        }
        if self.request.user.id:
            defaults['user'] = self.request.user

        try:
            if fcm_data['device_type'] == "ios":
                APNSDevice.objects.update_or_create(
                    device_id=fcm_data['device_id'], defaults=defaults)
            else:
                GCMDevice.objects.update_or_create(
                    device_id=fcm_data['device_id'], cloud_message_type='FCM', defaults=defaults)
        except:
            return Response({'error': {'device_id': ['device id is invalid']}}, status=400)

        return Response(serializer.data)


class ForgotPasswordAPI(APIView):

    def post(self, request, format=None):
        user_email = request.data['email']
        try:
            get_user = User.objects.get(email__iexact=user_email)
            if get_user:
                password = User.objects.make_random_password()
                get_user.set_password(password)
                get_user.save()
                subject = F"Updated forgot password"
                message = F"{user_email} Your Temparary Updated Password is: {password}"

                # send the email to the recipent
                send_mail(
                    subject=subject,
                    message=message,
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user_email]
                )
        except:
            return Response({'error': "Provided email don't exist."}, status=404)
        return Response({'status': True})
