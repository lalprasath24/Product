from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import login
from main.models import User, OTP
from .serilizerp import PhoneNumberSerializer, OTPSerializer, UserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp(request):
    serializer = PhoneNumberSerializer(data=request.data)
    
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        
        # Generate and save OTP
        otp_obj = OTP.generate_otp(phone_number)
        
        # In production, you would integrate with an SMS service here
        # For development, we'll just return the OTP in the response
        print(f"OTP for {phone_number}: {otp_obj.otp}")  # Remove this in production
        
        return Response({
            'message': 'OTP sent successfully',
            'phone_number': phone_number,
            # Remove the next line in production
            'otp': otp_obj.otp
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def verify_otp(request):
    serializer = OTPSerializer(data=request.data)
    
    if serializer.is_valid():
        phone_number = serializer.validated_data['phone_number']
        otp = serializer.validated_data['otp']
        
        # Get the OTP object
        otp_obj = OTP.objects.get(phone_number=phone_number, otp=otp)
        otp_obj.is_verified = True
        otp_obj.save()
        
        # Get or create user
        user, created = User.objects.get_or_create(phone_number=phone_number)
        
        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)
        
        return Response({
            'message': 'OTP verified successfully',
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            'created': created
        }, status=status.HTTP_200_OK)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)