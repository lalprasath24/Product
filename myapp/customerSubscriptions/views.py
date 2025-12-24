from django.shortcuts import render
from rest_framework import viewsets,status
from main.serilizers import CustomerSubscriptionsSerilizer
from main.models import CustomerSubscription
from rest_framework.decorators import action
from rest_framework.response import Response

# Create your views here.


class customerSubscriptionsViewSet(viewsets.ModelViewSet):
    queryset = CustomerSubscription.objects.all()
    serializer_class = CustomerSubscriptionsSerilizer
    lookup_field = 'pk'  
    
    
    @action(detail=True,methods=['post'])
    def activate(self,request,pk=None):
        subscription = self.get_object()
        subscription.status = CustomerSubscription.Status.ACTIVE
        subscription.save(update_fields=['status','updated_at'])
        return Response({'status : activated'},status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        subscription = self.get_object()
        subscription.status = CustomerSubscription.Status.CANCELLED
        subscription.save(update_fields=["status", "updated_at"])
        return Response({"status": "cancelled"}, status=status.HTTP_200_OK)
    
    @action(detail=False,methods=['get'])
    def active_subscriptions(self,request):
        customer_id = request.query_params.get("customer_id", None)
        if customer_id:
            active_subscriptions = CustomerSubscription.objects.filter(
                status=CustomerSubscription.Status.ACTIVE,
                customer_id = customer_id
            )
        else:
            active_subscriptions = CustomerSubscription.objects.filter(status=CustomerSubscription.Status.ACTIVE)    
        serilizer = self.get_serializer(active_subscriptions,many=True)
        return Response(data=serilizer.data,status=status.HTTP_200_OK)
         
    @action(detail=False,methods=['get'])
    def cancelled_subscriptions(self,request):
        customer_id = request.query_params.get("customer_id", None)
        if customer_id:
            active_subscriptions = CustomerSubscription.objects.filter(
                status=CustomerSubscription.Status.CANCELLED,
                customer_id = customer_id
            )
        else:
            active_subscriptions = CustomerSubscription.objects.filter(status=CustomerSubscription.Status.CANCELLED)    
        serilizer = self.get_serializer(active_subscriptions,many=True)
        return Response(data=serilizer.data,status=status.HTTP_200_OK)