from typing import Optional
import datetime
import decimal

from sqlalchemy import BigInteger, DECIMAL, Date, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.dialects.mysql import DATETIME, LONGTEXT, TINYINT
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Customers(Base):
    __tablename__ = 'customers'

    customer_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)

    customer_subscriptions: Mapped[list['CustomerSubscriptions']] = relationship('CustomerSubscriptions', back_populates='customer')
    customers_delivery_areas: Mapped[list['CustomersDeliveryAreas']] = relationship('CustomersDeliveryAreas', back_populates='customer')
    orders: Mapped[list['Orders']] = relationship('Orders', back_populates='customer')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='customer')



class DeliveryAreas(Base):
    __tablename__ = 'delivery_areas'

    area_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    area_name: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str] = mapped_column(String(20), nullable=False)
    is_serviced: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    area_code: Mapped[Optional[str]] = mapped_column(String(20))
    live_location: Mapped[Optional[str]] = mapped_column(String(2000))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    phone_number: Mapped[Optional[str]] = mapped_column(String(15))

    customers_delivery_areas: Mapped[list['CustomersDeliveryAreas']] = relationship('CustomersDeliveryAreas', back_populates='deliveryarea')


class Products(Base):
    __tablename__ = 'products'

    product_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    unit_type: Mapped[str] = mapped_column(String(10), nullable=False)
    unit_quantity: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    price_per_unit: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    current_stock: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_available: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    customer_subscriptions: Mapped[list['CustomerSubscriptions']] = relationship('CustomerSubscriptions', back_populates='product')
    order_items: Mapped[list['OrderItems']] = relationship('OrderItems', back_populates='product')


class Staff(Base):
    __tablename__ = 'staff'
    __table_args__ = (
        Index('phone', 'phone', unique=True),
    )

    staff_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    role: Mapped[str] = mapped_column(String(10), nullable=False)
    join_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(100))
    address: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    deliveries: Mapped[list['Deliveries']] = relationship('Deliveries', back_populates='delivered_by')


class SubscriptionPlans(Base):
    __tablename__ = 'subscription_plans'

    plan_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    plan_name: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    customer_subscriptions: Mapped[list['CustomerSubscriptions']] = relationship('CustomerSubscriptions', back_populates='plan')


class CustomerSubscriptions(Base):
    __tablename__ = 'customer_subscriptions'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
        ForeignKeyConstraint(['plan_id'], ['subscription_plans.plan_id']),
        ForeignKeyConstraint(['product_id'], ['products.product_id'])
    )

    subscription_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    start_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    end_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    daily_quantity: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    delivery_time_slot: Mapped[str] = mapped_column(String(50), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)
    payment_status: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)
    plan_id: Mapped[int] = mapped_column(Integer, nullable=False)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='customer_subscriptions')
    plan: Mapped['SubscriptionPlans'] = relationship('SubscriptionPlans', back_populates='customer_subscriptions')
    product: Mapped['Products'] = relationship('Products', back_populates='customer_subscriptions')
    deliveries: Mapped[list['Deliveries']] = relationship('Deliveries', back_populates='subscription')
    payments: Mapped[list['Payments']] = relationship('Payments', back_populates='subscription')


class CustomersDeliveryAreas(Base):
    __tablename__ = 'customers_delivery_areas'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
        ForeignKeyConstraint(['deliveryarea_id'], ['delivery_areas.area_id'])
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    deliveryarea_id: Mapped[int] = mapped_column(Integer, nullable=False)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='customers_delivery_areas')
    deliveryarea: Mapped['DeliveryAreas'] = relationship('DeliveryAreas', back_populates='customers_delivery_areas')


class Orders(Base):
    __tablename__ = 'orders'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
    )

    order_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_date: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    total_amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)
    delivery_address: Mapped[str] = mapped_column(LONGTEXT, nullable=False)
    payment_status: Mapped[str] = mapped_column(String(10), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delivery_date: Mapped[Optional[datetime.date]] = mapped_column(Date)
    delivery_time_slot: Mapped[Optional[str]] = mapped_column(String(50))
    notes: Mapped[Optional[str]] = mapped_column(LONGTEXT)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='orders')
    order_items: Mapped[list['OrderItems']] = relationship('OrderItems', back_populates='order')


class OrderItems(Base):
    __tablename__ = 'order_items'
    __table_args__ = (
        ForeignKeyConstraint(['order_id'], ['orders.order_id']),
        ForeignKeyConstraint(['product_id'], ['products.product_id'])
    )

    item_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    quantity: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    unit_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    total_price: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    order_id: Mapped[int] = mapped_column(Integer, nullable=False)
    product_id: Mapped[int] = mapped_column(Integer, nullable=False)

    order: Mapped['Orders'] = relationship('Orders', back_populates='order_items')
    product: Mapped['Products'] = relationship('Products', back_populates='order_items')


class Deliveries(Base):
    __tablename__ = 'deliveries'
    __table_args__ = (
        ForeignKeyConstraint(['delivered_by_id'], ['staff.staff_id']),
        ForeignKeyConstraint(['subscription_id'], ['customer_subscriptions.subscription_id'])
    )

    delivery_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    delivery_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    quantity: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    updated_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    subscription_id: Mapped[int] = mapped_column(Integer, nullable=False)
    delivery_notes: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    actual_delivery_time: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))
    delivered_by_id: Mapped[Optional[int]] = mapped_column(Integer)

    delivered_by: Mapped[Optional['Staff']] = relationship('Staff', back_populates='deliveries')
    subscription: Mapped['CustomerSubscriptions'] = relationship('CustomerSubscriptions', back_populates='deliveries')


class Payments(Base):
    __tablename__ = 'payments'
    __table_args__ = (
        ForeignKeyConstraint(['customer_id'], ['customers.customer_id']),
        ForeignKeyConstraint(['subscription_id'], ['customer_subscriptions.subscription_id'])
    )

    payment_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    amount: Mapped[decimal.Decimal] = mapped_column(DECIMAL(10, 2), nullable=False)
    payment_date: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    payment_method: Mapped[str] = mapped_column(String(15), nullable=False)
    status: Mapped[str] = mapped_column(String(10), nullable=False)
    customer_id: Mapped[int] = mapped_column(Integer, nullable=False)
    transaction_id: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(LONGTEXT)
    subscription_id: Mapped[Optional[int]] = mapped_column(Integer)

    customer: Mapped['Customers'] = relationship('Customers', back_populates='payments')
    subscription: Mapped[Optional['CustomerSubscriptions']] = relationship('CustomerSubscriptions', back_populates='payments')


class MainOtp(Base):
    __tablename__ = 'main_otp'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    phone_number: Mapped[str] = mapped_column(String(15), nullable=False)
    otp: Mapped[str] = mapped_column(String(6), nullable=False)
    created_at: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    is_verified: Mapped[int] = mapped_column(TINYINT(1), nullable=False)


class MainUser(Base):
    __tablename__ = 'main_user'
    __table_args__ = (
        Index('phone_number', 'phone_number', unique=True),
    )

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    password: Mapped[str] = mapped_column(String(128), nullable=False)
    phone_number: Mapped[str] = mapped_column(String(17), nullable=False)
    is_active: Mapped[int] = mapped_column(TINYINT(1), nullable=False)
    date_joined: Mapped[datetime.datetime] = mapped_column(DATETIME(fsp=6), nullable=False)
    last_login: Mapped[Optional[datetime.datetime]] = mapped_column(DATETIME(fsp=6))