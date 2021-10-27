from django.urls import path, re_path

from . import views

urlpatterns = [
    path('', views.UserUpdateView.as_view(), name='user_get_or_update'),
    path('delete-user/', views.UserUpdateView.as_view(), name='user_delete'),
    path('forgot-password/', views.ForgotPasswordAPI.as_view(),
         name='forgot_password'),
    path('signup/', views.RegisterUserView.as_view(), name='normal_register'),
    path('signin/', views.CutomObtainPairView.as_view(), name='noramal_signin'),
    path('signin/social-media/',
         views.SocialUserView.as_view(), name='social_media_signin'),
    path('signin/guest/', views.GuestUserView.as_view(),
         name='guest_user_signin'),
    path('feedback/', views.FeedbackAPI.as_view(), name="feedback"),
    path('device-register/', views.FcmTokenAPI.as_view(),
         name="device_fcm_register"),
]
