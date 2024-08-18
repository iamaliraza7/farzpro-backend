from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import User
from .serializers import UserSerializer
from utils.otp_generator import generate_otp

# Create your views here.

class UserSignUPView(APIView):
    """ View to signup a user """
    permission_classes = (AllowAny,)

    def post(self, request):
        """ function to login """
        if User.objects.filter(email = request.data['email']).exists():
            raise ValidationError("User already exists with this email")
        try:
            user_data = {
                "email": request.data['email'],
                "first_name": request.data['first_name'],
                "last_name": request.data['last_name'],
                "username": request.data['email'],
            }
            UserSerializer(data = user_data).is_valid(raise_exception = True)
            user_obj = User(**user_data)
            user_obj.set_password(request.data['password'])
            user_obj.save()
            user_data = UserSerializer(user_obj).data
            return Response(user_data)
        except Exception as e:
            raise ValidationError(e)
        
class ForgotPasswordView(APIView):
    """ View to Forgot Password """
    permission_classes = (AllowAny,)

    def post(self, request):
        """ function to forgot password """
        if User.objects.filter(email = request.data['email']).exists() == False:
            raise ValidationError("No any user exists with this email")
        
        user_obj = User.objects.get(email = request.data['email'])
        user_obj.otp = generate_otp()
        user_obj.save()

        return Response({"otp": user_obj.otp})
class ResetPasswordView(APIView):
    """ View to reset the user's password """
    permission_classes = (AllowAny,)

    def post(self, request):
        """ Function to reset password """
        email = request.data.get('email')
        otp = request.data.get('otp')
        new_password = request.data.get('password')

        # Validate request data
        if not email or not otp or not new_password:
            raise ValidationError("Email, OTP, and new password are required")

        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User does not exist with this email")

        # Check if the OTP is correct
        if user_obj.otp != otp:
            raise ValidationError("Invalid OTP")

        # Set the new password
        user_obj.set_password(new_password)
        user_obj.otp = None  # Clear the OTP after successful password reset
        user_obj.save()

        return Response({"message": "Password has been reset successfully"})