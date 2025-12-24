from django.urls import path,include
from rest_framework.routers import DefaultRouter
from customer.views import CustomerView,CustomerDetailsView
from product import views as productview
from subscriptions import views as subscriptionsViews
from customerSubscriptions.views import customerSubscriptionsViewSet
from login import views as loginviews
from delivery.views import DeliveryAreaViewSet
from analytics.views import month_wise_customer_analytics,delivery_area_based_customers
from Email.views import EmailTestingAPI


router = DefaultRouter()


# //customer_subscriptions
router.register('customer-subscriptions',customerSubscriptionsViewSet,basename='customer-subscriptions')
router.register('deliveryArea',DeliveryAreaViewSet,basename='deliveryArea')

urlpatterns = [  
    
    path('',include(router.urls)),
    # //Customers             
    path('customers/',CustomerView.as_view()),
    path('customers/<int:pk>/',CustomerDetailsView.as_view()),
    
    # //Product
    
    path('products/',productview.ProductListCreateAPIView.as_view()),
    path('products/<int:pk>',productview.ProductRetrieveUpdateDestroyAPIView.as_view()),
    
    # //subscriptions
    path('subscriptionPlan/',subscriptionsViews.SubscriptionPlanListCreateAPIView.as_view()),
    path('subscriptionPlan/<int:pk>',subscriptionsViews.SubscriptionPlanRetrieveUpdateDestroyAPIView.as_view()),
    
    # //login
    path('send-otp/', loginviews.send_otp, name='send_otp'),
    path('verify-otp/', loginviews.verify_otp, name='verify_otp'),
    path('profile/', loginviews.user_profile, name='user_profile'),
    
    # Analyticals and excel reports.
    
    path('month_wise_customer_analytics/',month_wise_customer_analytics,name='month_wise_customer_analytics'),
    path('delivery_area_based_customers/',delivery_area_based_customers,name='delivery_area_based_customers'),
    
    #Email
    
    path('email_testing_api/',EmailTestingAPI,name='new_customer_to_delivery_area')
    
]
