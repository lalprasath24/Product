from django.shortcuts import render
from rest_framework.decorators import api_view
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from  myapp import settings
from rest_framework.response import Response
from rest_framework import status
from main.models import DeliveryArea
import logging

logger = logging.getLogger('myapp')


# Create your views here.
# Email Testing API
@api_view(['POST'])
def EmailTestingAPI(request):
    subject = "Welcome to My App"
    message = "Hello! Thanks for signing up."
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ['lalptasathk187@gmail.com']
    send_mail(subject, message, from_email, recipient_list)
    return Response({"message": "Email sent successfully!"})



def new_customer_to_delivery_area(customers):
    logger.info('new_customer_to_delivery_area started')
    email_subject = "🎉 New Customer"
    delivery_area_id = []
    
    rows = ""
    for cust in customers:
        first_area = cust.delivery_areas.first()   # gets the first related area
        if first_area:
            delivery_area_id.append(first_area.area_id)
        rows += f"""
        <tr>
            <td style="padding: 8px; border: 1px solid #ddd;">{cust.first_name}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{cust.email}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{cust.phone}</td>
            <td style="padding: 8px; border: 1px solid #ddd;">{cust.address}</td>
        </tr>
        """

    html_message = f"""
    <html>
        <body style="font-family: Arial, sans-serif; background-color:#f8f9fa; padding:20px;">
            <div style="background:#ffffff; padding:20px; border-radius:10px; box-shadow:0 2px 8px rgba(0,0,0,0.1);">
                <h2 style="color:#007bff;">New Customer(s) Added Successfully</h2>
                <p>The following customer details have been added to the system:</p>

                <table style="border-collapse:collapse; width:100%; font-size:14px; margin-top:10px;">
                    <thead>
                        <tr style="background-color:#007bff; color:white;">
                            <th style="padding:8px; border:1px solid #ddd;">Name</th>
                            <th style="padding:8px; border:1px solid #ddd;">Email</th>
                            <th style="padding:8px; border:1px solid #ddd;">Phone</th>
                            <th style="padding:8px; border:1px solid #ddd;">Address</th>
                        </tr>
                    </thead>
                    <tbody>
                        {rows}
                    </tbody>
                </table>

                <p style="margin-top:20px; color:#555;">Thanks,<br><strong>Your Delivery System</strong></p>
            </div>
        </body>
    </html>
    """

    
    if delivery_area_id:
        delivery_area = DeliveryArea.objects.filter(area_id=delivery_area_id[0]).first()
    else:
        logger.error("⚠️ No delivery area found for customers.")
        return

    if not delivery_area or not delivery_area.email:
        logger.error("⚠️ No valid email found for the delivery area.")
        return
    
    
    text_message = "New customer(s) have been added successfully."
    

    email = EmailMultiAlternatives(
        subject=email_subject,
        body=text_message,
        from_email=settings.EMAIL_HOST_USER,
        to=[delivery_area.email],  
    )
    email.attach_alternative(html_message, "text/html")
    email.send(fail_silently=False)
    logger.info("Email send sucessfully")
