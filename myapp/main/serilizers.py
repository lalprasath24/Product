from main.models import Customer, Product, SubscriptionPlan,CustomerSubscription
from rest_framework import serializers


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'  
        
class ProductSerilizer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields ='__all__'        

class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'
    
    def validate_plan_name(self, value):
        if SubscriptionPlan.objects.filter(plan_name=value).exists():
            raise serializers.ValidationError("Plan name should be unique")
        return value

    def validate(self, attrs):
        if attrs.get("price") <= 0:
            raise serializers.ValidationError({"price": "Price must be greater than 0"})

        if attrs.get("duration_days") < 7:
            raise serializers.ValidationError({"duration_days": "Duration must be at least 7 days"})

        if attrs.get("plan_name") == "Free" and attrs.get("price") > 0:
            raise serializers.ValidationError("Free plan cannot have a price")

        return attrs 
    


class CustomerSubscriptionsSerilizer(serializers.ModelSerializer):
    class Meta:
        model =  CustomerSubscription
        fields = '__all__'    