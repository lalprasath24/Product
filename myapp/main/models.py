from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.validators import RegexValidator
import random
import datetime


class UserManager(BaseUserManager):
    def create_user(self, phone_number, **extra_fields):
        if not phone_number:
            raise ValueError('Phone number is required')
        user = self.model(phone_number=phone_number, **extra_fields)
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    
    phone_number = models.CharField(
        validators=[phone_regex], max_length=17, unique=True
    )
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def __str__(self):
        return self.phone_number

class OTP(models.Model):
    phone_number = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_expired(self):
        expiration_time = self.created_at + datetime.timedelta(minutes=10)
        return timezone.now() > expiration_time
    
    @classmethod
    def generate_otp(cls, phone_number):
        cls.objects.filter(phone_number=phone_number).delete()
        
        otp = str(random.randint(100000, 999999))
        
        return cls.objects.create(phone_number=phone_number, otp=otp)
    
    def __str__(self):
        return f"{self.phone_number} - {self.otp}"



class Customer(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'
    
    class Type(models.TextChoices):
        REGULAR = 'regular', 'Regular'
        PREMIUM = 'premium', 'Premium'
        ADMIN = 'admin', 'Admin'
    
    customer_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50, null=True,blank=True)
    last_name = models.CharField(max_length=50, null=True,blank=True)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, unique=True, blank=True, null=True)
    address = models.TextField(null=True, blank=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=50, null=True,blank=True)
    pincode = models.CharField(max_length=20, null=True,blank=True)
    hashed_password = models.CharField(max_length=255, null=True,blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    type = models.CharField(max_length=10, choices=Type.choices, default=Type.REGULAR)
    language = models.CharField(max_length=10, default='en')
    last_login_on = models.DateTimeField(blank=True, null=True)
    passwd_changed_on = models.DateTimeField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True,blank=True)
    updated_on = models.DateTimeField(auto_now=True,blank=True)
    
    delivery_areas = models.ManyToManyField('DeliveryArea',related_name='customers')
    
    def set_password(self, raw_password):
        self.hashed_password = make_password(raw_password)
        self.passwd_changed_on = timezone.now()
    
    def check_password(self, raw_password):
        return check_password(raw_password, self.hashed_password)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'customers'
        verbose_name = 'Customer'
        verbose_name_plural = 'Customers'

class Product(models.Model):
    class UnitType(models.TextChoices):
        LITER = 'liter', 'Liter'
        ML = 'ml', 'Milliliter'
        KG = 'kg', 'Kilogram'
        PACKET = 'packet', 'Packet'
    
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    unit_type = models.CharField(max_length=10, choices=UnitType.choices)
    unit_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    current_stock = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.product_name
    
    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'
        
        

class SubscriptionPlan(models.Model):
    plan_id = models.AutoField(primary_key=True)
    plan_name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    duration_days = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.plan_name
    
    class Meta:
        db_table = 'subscription_plans'
        verbose_name = 'Subscription Plan'
        verbose_name_plural = 'Subscription Plans'

class CustomerSubscription(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        PAUSED = 'paused', 'Paused'
        CANCELLED = 'cancelled', 'Cancelled'
        COMPLETED = 'completed', 'Completed'
    
    class PaymentStatus(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'
        PARTIAL = 'partial', 'Partial'
    
    subscription_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    daily_quantity = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='subscriptions')
    delivery_time_slot = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Subscription #{self.subscription_id} - {self.customer}"
    
    class Meta:
        db_table = 'customer_subscriptions'
        verbose_name = 'Customer Subscription'
        verbose_name_plural = 'Customer Subscriptions'

class Staff(models.Model):
    class Role(models.TextChoices):
        DELIVERY = 'delivery', 'Delivery'
        ADMIN = 'admin', 'Admin'
        MANAGER = 'manager', 'Manager'
    
    class Status(models.TextChoices):
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
    
    staff_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    role = models.CharField(max_length=10, choices=Role.choices)
    join_date = models.DateField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    class Meta:
        db_table = 'staff'
        verbose_name = 'Staff'
        verbose_name_plural = 'Staff'

class Delivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
        MISSED = 'missed', 'Missed'
    
    delivery_id = models.AutoField(primary_key=True)
    subscription = models.ForeignKey(CustomerSubscription, on_delete=models.CASCADE, related_name='deliveries')
    delivery_date = models.DateField()
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    delivered_by = models.ForeignKey(Staff, on_delete=models.SET_NULL, null=True, blank=True, related_name='deliveries')
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    delivery_notes = models.TextField(blank=True, null=True)
    actual_delivery_time = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery #{self.delivery_id} - {self.subscription}"
    
    class Meta:
        db_table = 'deliveries'
        verbose_name = 'Delivery'
        verbose_name_plural = 'Deliveries'

class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Card'
        UPI = 'upi', 'UPI'
        NETBANKING = 'netbanking', 'Net Banking'
        WALLET = 'wallet', 'Wallet'
    
    class Status(models.TextChoices):
        SUCCESS = 'success', 'Success'
        FAILED = 'failed', 'Failed'
        PENDING = 'pending', 'Pending'
    
    payment_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='payments')
    subscription = models.ForeignKey(CustomerSubscription, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=15, choices=PaymentMethod.choices)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Payment #{self.payment_id} - {self.customer}"
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'Pending'
        CONFIRMED = 'confirmed', 'Confirmed'
        DELIVERED = 'delivered', 'Delivered'
        CANCELLED = 'cancelled', 'Cancelled'
    
    class PaymentStatus(models.TextChoices):
        PAID = 'paid', 'Paid'
        UNPAID = 'unpaid', 'Unpaid'
        PARTIAL = 'partial', 'Partial'
    
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING)
    delivery_address = models.TextField()
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time_slot = models.CharField(max_length=50, blank=True, null=True)
    payment_status = models.CharField(max_length=10, choices=PaymentStatus.choices, default=PaymentStatus.UNPAID)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.order_id} - {self.customer}"
    
    class Meta:
        db_table = 'orders'
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

class OrderItem(models.Model):
    item_id = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"Item #{self.item_id} - {self.product}"
    
    class Meta:
        db_table = 'order_items'
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

class DeliveryArea(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=100)    
    area_code = models.CharField(max_length=20,null=True)
    pincode = models.CharField(max_length=20)
    live_location = models.CharField(max_length=2000,null=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)   
    is_serviced = models.BooleanField(default=True)
    
    
    def __str__(self):
        return f"{self.area_name} - {self.pincode}"
    
    class Meta:
        db_table = 'delivery_areas'
        verbose_name = 'Delivery Area'
        verbose_name_plural = 'Delivery Areas'