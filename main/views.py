from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.conf import settings
from .serializer import LoginSerializer
from django.core.cache import cache
from .sms import send_verification_code
from django.contrib.auth import get_user_model
from .serializer import RegisterUserSerializer

User = get_user_model()


class LoginView(APIView):
    def post(self, request):

        # phone number is saved in sessions
        # here we check if password and sessioned phone number match
        phone = request.session.get('Phone')
        if not phone:
            return Response({"error": "Phone number not found in session."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            password = serializer.validated_data['password']
            user = authenticate(request, Phone=phone, password=password)
            if user is not None:
                login(request, user)
                cache.set(self.get_client_ip(request), 0, timeout=settings.FAILED_ATTEMPTS_RESET_TIMEOUT)
                return Response({"message": "Logged in successfully."}, status=status.HTTP_200_OK)
            else:
                ip = self.get_client_ip(request)
                failed_attempts = cache.get(ip, 0) + 1
                cache.set(ip, failed_attempts, timeout=settings.FAILED_ATTEMPTS_RESET_TIMEOUT)
                if failed_attempts >= 3:
                    return Response({'error': 'Too many failed login attempts. Try again later.'},
                                    status=status.HTTP_403_FORBIDDEN)
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class IdentifyView(APIView):
    def post(self, request):
        phone = request.data.get('Phone')
        if not phone:
            return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the phone number is registered
        try:
            user = User.objects.get(Phone=phone)
            request.session['Phone'] = phone
            return Response({"message": "Phone number accepted. enter pass word."}, status=status.HTTP_200_OK)

        except User.DoesNotExist:

            # Phone number not registered, send verification code
            request.session['Phone'] = phone
            verification_code = send_verification_code(phone)
            cache.set(phone, verification_code, timeout=300)  # Cache the verification code for 5 minutes
            return Response({"message": "Phone number not registered. Verification code sent. Please enter the code."},
                            status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other potential errors
            return Response({"error": "An unexpected error occurred. Please try again later."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SendVerificationCodeView(APIView):
    def post(self, request):
        phone_number = request.session.get('Phone')
        if not phone_number:
            return Response({"error": "Phone number is required"}, status=status.HTTP_400_BAD_REQUEST)

        verification_code = request.data.get('verification_code')
        if not phone_number or not verification_code:
            return Response({"error": "Phone number and verification code are required"},
                            status=status.HTTP_400_BAD_REQUEST)

        cached_code = cache.get(phone_number)
        if cached_code is None:

            return Response({"error": "Verification code has expired or is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

        if str(cached_code) == str(verification_code):
            return Response({"message": "Verification successful"}, status=status.HTTP_200_OK)
        else:
            ip = self.get_client_ip(request)
            failed_attempts = cache.get(ip, 0) + 1
            cache.set(ip, failed_attempts, timeout=settings.FAILED_ATTEMPTS_RESET_TIMEOUT)
            if failed_attempts >= 3:
                return Response({'error': 'Too many failed login attempts. Try again later.'},
                                status=status.HTTP_403_FORBIDDEN)
            return Response({"error": "Invalid verification code"}, status=status.HTTP_400_BAD_REQUEST)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


class RegisterView(APIView):
    def post(self, request):
        # Get phone number from session
        phone = request.session.get('Phone')
        if not phone:
            return Response({"error": "Phone number not found in session."}, status=status.HTTP_400_BAD_REQUEST)

        # Deserialize and validate the request data
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            name = serializer.validated_data['name']
            lastname = serializer.validated_data['last_name']
            email = serializer.validated_data['email']
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            # Create the new user
            phone = request.session.get('Phone')
            user = User.objects.create_user(username=username, first_name=name, last_name=lastname,
                                            email=email, password=password, Phone=phone)
            user.save()

            return Response({"message": "User created successfully."}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
