from rest_framework import serializers
from django.contrib.auth import authenticate
from main.models import User, OTP

class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    
    def validate_phone_number(self, value):
        # Add phone number validation logic if needed
        return value

class OTPSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)
    otp = serializers.CharField(max_length=6)
    
    def validate(self, data):
        phone_number = data.get('phone_number')
        otp = data.get('otp')
        
        try:
            otp_obj = OTP.objects.get(phone_number=phone_number, otp=otp)
            
            if otp_obj.is_expired():
                raise serializers.ValidationError("OTP has expired")
                
            if otp_obj.is_verified:
                raise serializers.ValidationError("OTP already used")
                
        except OTP.DoesNotExist:
            raise serializers.ValidationError("Invalid OTP")
        
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'phone_number', 'date_joined']