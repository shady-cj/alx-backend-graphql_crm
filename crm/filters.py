import django_filters as filters


from .models import Customer, Product, Order
from django.db.models import Sum


class CustomerFilter(filters.FilterSet):
    name_icontains = filters.CharFilter(field_name="name", lookup_expr='icontains')
    email = filters.CharFilter(field_name="email", lookup_expr='icontains')
    phone_pattern = filters.CharFilter(field_name="phone", lookup_expr='regex')
    created_at_lte = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    created_at_gte = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')


    class Meta:
        model = Customer
        fields = []

class ProductFilter(filters.FilterSet):
    name_icontains = filters.CharFilter(field_name="name", lookup_expr='icontains')
    price_lte = filters.NumberFilter(field_name="price", lookup_expr='lte')
    price_gte = filters.NumberFilter(field_name="price", lookup_expr='gte')
    stock_lte = filters.NumberFilter(field_name="stock", lookup_expr='lte')
    stock_gte = filters.NumberFilter(field_name="stock", lookup_expr='gte')
    created_at_lte = filters.DateTimeFilter(field_name="created_at", lookup_expr='lte')
    created_at_gte = filters.DateTimeFilter(field_name="created_at", lookup_expr='gte')
    
    order_by = filters.OrderingFilter(fields=(
        ("name", "product_name"),
        ("price", "product_price"),
        ("stock", "stock")
    ))

    # price = filters.RangeFilter(field_name="price")
    # stock = filters.RangeFilter(field_name="stock")
    # created_at = filters.DateTimeFromToRangeFilter(field_name="created_at")
    class Meta:
        model = Product
        fields = []

class OrderFilter(filters.FilterSet):
    # order_date = filters.DateTimeFromToRangeFilter(field_name="order_date")
    customer_name = filters.CharFilter(field_name="customer_id__name", lookup_expr='icontains')
    order_date_lte = filters.DateTimeFilter(field_name="order_date", lookup_expr='lte')
    order_date_gte = filters.DateTimeFilter(field_name="order_date", lookup_expr='gte')
    product_name = filters.CharFilter(field_name="product_ids__name", lookup_expr='icontains')
    total_amount_lte = filters.NumberFilter(method='filter_total_amount_lte')
    total_amount_gte = filters.NumberFilter(method='filter_total_amount_gte')

    order_by = filters.OrderingFilter(fields=(
        ("product_ids__name", "product_name"),
        ("product_ids__price", "product_price"),
        ("order_date", "order_date"),
    ))


    class Meta:
        model = Order
        fields = [] 

    def filter_total_amount_lte(self, queryset, name, value):
        return queryset.annotate(total_amount=Sum('product_ids__price')).filter(total_amount__lte=value)

    def filter_total_amount_gte(self, queryset, name, value):
        return queryset.annotate(total_amount=Sum('product_ids__price')).filter(total_amount__gte=value)