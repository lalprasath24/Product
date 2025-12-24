from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings



class APIKeyAuthentication(BaseAuthentication):
    def authenticate(self,request):
        api_key = request.headers.get("X-API-KEY")
        
        if not api_key:
            raise AuthenticationFailed("API Key required")
        if api_key !=settings.API_KEY:
            raise AuthenticationFailed("Invalid API Key")
        return (None,None)
        