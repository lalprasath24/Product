from django.shortcuts import render
from rest_framework import viewsets
from main.models import DeliveryArea
from .serilizer import DeliveryAreaSerilizer
# Create your views here.

class DeliveryAreaViewSet(viewsets.ModelViewSet):
    queryset = DeliveryArea.objects.all()
    serializer_class = DeliveryAreaSerilizer
    lookup_field ='pk'