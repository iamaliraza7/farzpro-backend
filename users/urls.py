from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import *

urlpatterns = [
    path('signup/', UserSignUPView.as_view(), name="signup_for_a_user"),
    path('login/', TokenObtainPairView.as_view(), name="get_token_with_email_password"),
    path('forgot-password/', ForgotPasswordView.as_view(), name="forgot_password"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset_password")
]