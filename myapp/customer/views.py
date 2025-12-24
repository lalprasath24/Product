from django.shortcuts import render
from rest_framework.views import APIView
from main.models import Customer
from main.serilizers import CustomerSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import NotFound,APIException
from Email.views import new_customer_to_delivery_area



# Customer Profile

class CustomerView(APIView):
    def get(self,request):
        try:
            customer_obj = Customer.objects.all()
        except :
            raise  NotFound(detail='customers not exists')
        customer_data = CustomerSerializer(customer_obj,many=True)
        return Response(data=customer_data.data,status=status.HTTP_200_OK)
    
    def post(self,request):
        customer_save_obj =CustomerSerializer(data=request.data,many=True)
        if customer_save_obj.is_valid():
            customers=customer_save_obj.save()
            new_customer_to_delivery_area(customers)
            return Response(status=status.HTTP_201_CREATED)
        return Response(customer_save_obj.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    
class CustomerDetailsView(APIView):
    def get_customer(self,pk):
        try:
            customer_obj = Customer.objects.get(pk=pk)
            return customer_obj
        except Exception as e: 
            raise APIException(detail=f'get_customer : {e}')
    def get(self,request,pk):
        customer_obj = self.get_customer(pk)
        customer_data = CustomerSerializer(customer_obj)
        return Response(data=customer_data.data,status=status.HTTP_200_OK)
        
    def put(self,request,pk):
       customer_obj = self.get_customer(pk)
       put_serilizer = CustomerSerializer(customer_obj,data=request.data)
       if put_serilizer.is_valid():
           put_serilizer.save()
           return Response(status=status.HTTP_202_ACCEPTED)
       return Response(data=put_serilizer.errors,status=status.HTTP_406_NOT_ACCEPTABLE)
    
    def delete(self,request,pk):
        try:
            customer_obj = self.get_customer(pk)
            customer_obj.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as ex:
            raise APIException(f"{ex}")   
        
        
        
       
     
     
       