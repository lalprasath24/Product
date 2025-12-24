from rest_framework import serializers
from main.models import DeliveryArea


class DeliveryAreaSerilizer(serializers.ModelSerializer):
    class Meta:
        model = DeliveryArea
        fields ='__all__'
    
    def validate(self, attrs):
        area_name = attrs.get('area_name')
        area_code = attrs.get('area_code')
        
        if DeliveryArea.objects.filter(area_name=area_name).exists():
            raise serializers.ValidationError({"area_name": "This area name already exists."})
        if DeliveryArea.objects.filter(area_code=area_code).exists():
            raise serializers.ValidationError({"area_code": "This area code already exists."})
        return attrs
             
   