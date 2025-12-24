from django.shortcuts import render
from main.models import Product
from main.serilizers import ProductSerilizer
from rest_framework import generics

# Create your views here.

class ProductListCreateAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    
class ProductRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerilizer
    lookup_field = 'pk'
        