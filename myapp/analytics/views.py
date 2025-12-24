from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from django.http import HttpResponse,JsonResponse
from main.models import Customer
from main.serilizers import CustomerSerializer
from rest_framework.response import Response
from django.db import connection
import openpyxl

# Create your views here.
@api_view(['GET'])
def month_wise_customer_analytics(request):
    
    year = request.query_params.get('year')
    month = request.query_params.get('month')
    deliveryarea_id = request.query_params.get('deliveryarea_id')    
    
    if deliveryarea_id is not None:
        query = f"""SELECT c.customer_id, c.first_name, c.last_name, cda.deliveryarea_id
        FROM customers c
        JOIN customers_delivery_areas cda
        ON c.customer_id = cda.customer_id
        WHERE cda.deliveryarea_id = {deliveryarea_id}"""
        
        with connection.cursor() as cursor:
            cursor.execute(query)
            columns = [col[0] for col in cursor.description]
            data = [dict(zip(columns, row)) for row in cursor.fetchall()]
            return Response(data)
        
        
    
    customer_data = Customer.objects.filter(
        created_on__year=year,
        created_on__month =month
    )
    
    serilized_data = CustomerSerializer(customer_data,many=True)    
    return Response(serilized_data.data)


@api_view(['GET'])
def delivery_area_based_customers(request):
    
    query = """SELECT cda.deliveryarea_id, c.*
    FROM customers_delivery_areas AS cda
    JOIN customers AS c
    ON c.customer_id = cda.customer_id
    ORDER BY cda.deliveryarea_id"""
    
    excel = request.query_params.get('excel')
    
    with connection.cursor() as cursor:
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()
        resultdata = [dict(zip(columns, row)) for row in rows]
        data = [row for row in rows] 
    
    if excel == 'true':
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title='Delivery_area_based_customers'
        headers = ['deliveryarea_id', 'customer_id', 'first_name', 'last_name',
                    'phone', 'email', 'address', 'landmark', 'city', 'pincode',
                    'hashed_password', 'status', 'type', 'language', 'last_login_on',
                    'passwd_changed_on', 'notes', 'created_on', 'updated_on']
        ws.append(headers)
        for data in data:
            ws.append(data)
            
        response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        )
        response['Content-Disposition'] = 'attachment; filename=delivery_area_based_customers.xlsx'
        wb.save(response)
        return response 
    return Response(resultdata)




        