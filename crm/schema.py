from graphene_django import DjangoObjectType, DjangoListField
import graphene
from graphene_django.filter import DjangoFilterConnectionField
from .models import Customer, Order
from crm.models import Product
import re
from graphql import GraphQLError
from django.utils import timezone
from .filters import CustomerFilter, ProductFilter, OrderFilter

class CustomerNode(DjangoObjectType):
    class Meta:
        model = Customer
        interfaces = (graphene.relay.Node, )
        filterset_class = CustomerFilter

class ProductNode(DjangoObjectType):
    class Meta:
        model = Product
        interfaces = (graphene.relay.Node, )
        filterset_class = ProductFilter

class OrderNode(DjangoObjectType):
    class Meta:
        model = Order
        interfaces = (graphene.relay.Node, )
        filterset_class = OrderFilter
    
class CustomerType(DjangoObjectType):
    class Meta:
        model = Customer
        


class ProductType(DjangoObjectType):
    class Meta:
        model = Product


class OrderType(DjangoObjectType):
    customer = graphene.Field(CustomerType)
    products = DjangoListField(ProductType)
    totalAmount = graphene.Decimal()

    class Meta:
        model = Order

    def resolve_customer(root, info):
        return root.customer_id

    def resolve_products(root, info):
        return root.product_ids

    def resolve_totalAmount(root, info):
        amount = 0
        for product in root.product_ids.all():
            amount += product.price
        return amount


class CreateCustomer(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        email = graphene.String(required=True)
        phone = graphene.String()

    customer = graphene.Field(CustomerType)
    message = graphene.String()

    def mutate(self, info, name, email, phone=None):
        phone_re = re.compile(r"(^\+\d{10}$)|(\d{3}-\d{3}-\d{4}$)")
        if phone_re.match(phone) is None:
            raise GraphQLError("Phone number is invalid")

        if Customer.objects.filter(email=email).exists():
            raise GraphQLError("Email already exists")

        customer = Customer(name=name, email=email, phone=phone)
        customer.save()
        return CreateCustomer(
            customer=customer, message="Customer Created Successfully"
        )


class CustomerInput(graphene.InputObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    phone = graphene.String()


class CustomerBulkErrorType(graphene.ObjectType):
    name = graphene.String(required=True)
    email = graphene.String(required=True)
    error_message = graphene.String(required=True)


class BulkCreateCustomers(graphene.Mutation):
    customers = graphene.List(CustomerType)
    errors = graphene.List(CustomerBulkErrorType)

    class Arguments:
        customers = graphene.List(graphene.NonNull(CustomerInput), required=True)

    def mutate(self, info, customers):
        phone_re = re.compile(r"(^\+\d{10}$)|(\d{3}-\d{3}-\d{4}$)")

        customer_list = []
        errors = []
        for customer in customers:
            name = customer.get("name")
            email = customer.get("email")
            phone = customer.get("phone")
            failed = False
            error_message = None
            if phone and phone_re.match(phone) is None:
                error_message = "Phone number is invalid"
                failed = True

            if Customer.objects.filter(email=email).exists():
                error_message = "Email already exists"
                failed = True
            if failed:
                errors.append(
                    {"name": name, "email": email, "error_message": error_message}
                )
            else:
                customer = Customer(name=name, email=email, phone=phone)
                customer_list.append(customer)
        created_customers = Customer.objects.bulk_create(customer_list)
        return BulkCreateCustomers(customers=created_customers, errors=errors)


class CreateProduct(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        price = graphene.Decimal(required=True)
        stock = graphene.Int(default_value=0)

    product = graphene.Field(ProductType)
    message = graphene.String()

    def mutate(self, info, name, price, stock=0):
        print(price, type(price))
        if price > 0 and stock >= 0:
            product = Product(name=name, price=price, stock=stock)
            product.save()
            return CreateProduct(
                product=product, message="Product Created Successfully"
            )
        raise GraphQLError("Validation error with price and stock")


class CreateOrder(graphene.Mutation):
    class Arguments:
        customer_id = graphene.String(required=True)
        product_ids = graphene.List(graphene.NonNull(graphene.String), required=True)
        order_date = graphene.DateTime(default_value=timezone.now())

    order = graphene.Field(OrderType)
    message = graphene.String()

    def mutate(self, info, customer_id, product_ids, order_date):
        if not Customer.objects.filter(id=customer_id).exists():
            raise GraphQLError("customer_id doesn't exist")
        product_ids = list(set(product_ids))
        p = Product.objects.filter(id__in=product_ids)
        if len(p) != len(product_ids):
            raise GraphQLError("One or more product_id doesn't exist")
        order = Order.objects.create(
            customer_id=Customer.objects.get(id=customer_id), order_date=order_date
        )
        order.product_ids.set(p)
        return CreateOrder(order=order, message="Order Created Successfully")



class UpdateLowStockProducts(graphene.Mutation):
    products = graphene.List(ProductType)

    def mutate(self, info):
        from django.db.models import F

        Product.objects.filter(stock__lt=10).update(stock=F('stock') + 10)
        
        return UpdateLowStockProducts(products=Product.objects.all())


class Mutation(graphene.ObjectType):
    create_order = CreateOrder.Field()
    create_customer = CreateCustomer.Field()
    bulk_create_customer = BulkCreateCustomers.Field()
    create_product = CreateProduct.Field()
    update_low_stock_products = UpdateLowStockProducts.Field()


class Query(graphene.ObjectType):
    customers = graphene.List(CustomerType)
    orders = graphene.List(OrderType)
    products = graphene.List(ProductType)
    all_customers = DjangoFilterConnectionField(CustomerNode)
    all_orders = DjangoFilterConnectionField(OrderNode)
    all_products = DjangoFilterConnectionField(ProductNode)
    total_customers = graphene.Int()
    total_orders = graphene.Int()
    total_revenue = graphene.Decimal()

    # def resolve_all_products(root, info, filter=None, **kwargs):
    #     qs = Product.objects.all()
    #     if filter:
    #         filterset = ProductFilter(data=filter, queryset=qs)
    #         if filterset.is_valid():
    #             return filterset.qs
    #         else:
    #             raise GraphQLError(f"Invalid filter: {filterset.errors}")
        # return qs

    def resolve_customers(root, info):
        return Customer.objects.all()

    def resolve_orders(root, info):
        return Order.objects.all()

    def resolve_products(root, info):
        return Product.objects.all()

    def resolve_total_customers(root, info):
        return Customer.objects.count()
    def resolve_total_orders(root, info):
        return Order.objects.count()
    def resolve_total_revenue(root, info):
        from django.db.models import Sum
        revenue = Order.objects.aggregate(total_revenue=Sum('product_ids__price'))['total_revenue']
        return revenue if revenue else 0