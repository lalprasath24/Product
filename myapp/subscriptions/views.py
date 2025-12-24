from django.shortcuts import render
from main.models import SubscriptionPlan
from main.serilizers import SubscriptionPlanSerializer
from rest_framework import generics
# Create your views here.


class SubscriptionPlanListCreateAPIView(generics.ListCreateAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer

class SubscriptionPlanRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer
    lookup_field ='pk'
        