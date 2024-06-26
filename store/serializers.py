from decimal import Decimal
from django.db import transaction
from rest_framework import serializers
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, ProductImage, Review
from .signals import order_created

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title', 'products_count']

    products_count = serializers.IntegerField(read_only=True)
        
class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review  
        fields = ['id', 'date', 'name', 'description' ]

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id, ** validated_data)

    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return ProductImage.objects.create(product_id=product_id,**validated_data)
    

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=6, decimal_places=2, source='unit_price')
    price_with_tax = serializers.SerializerMethodField(method_name="calculate_tax")
    images = ProductImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Product
        fields = ['id', 'title', 'price', 'collection', 'price_with_tax', 'description', 'images']
    
    def calculate_tax(self, product : Product):
        return product.unit_price * Decimal(1.1)

class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name="calculate_total_price")
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def calculate_total_price(self, cartitem : CartItem):
        return cartitem.product.unit_price * cartitem.quantity


#Cart Serializer:
class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()
    
    class Meta:
        model = Cart
        fields = ['id', 'items', 'total_price'] 

    def get_total_price(self, cart : Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id (self, value):
        if not Product.objects.filter(pk = value).exists():
            raise serializers.ValidationError('No Product with given id was found')
        return value

    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']

        try:
            cart_item = CartItem.objects.get(cart_id = cart_id, product_id = product_id)
            cart_item.quantity += quantity
            self.instance = cart_item
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)
            
        return self.instance
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']


    
class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields =  ['quantity']


class CustomerSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Customer
        fields = ['id', 'user_id', 'phone', 'birth_date', 'membership']

class OrderItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'unit_price', 'quantity']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'placed_at', 'payment_status', 'customer', 'items']

class CreateOrderSerializer(serializers.Serializer):#Create an order from a cart
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        print('triger')
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError('No card with given id was found')
        if CartItem.objects.filter(cart_id=cart_id).count()==0:
            raise serializers.ValidationError('This card is empty')
        return cart_id

    def save(self, **kwargs):
        with transaction.atomic(): 
            cart_id = self.validated_data['cart_id']

            user_id = self.context['user_id']
            (customer, createdOrNot)  = Customer.objects.\
                get_or_create(user_id = user_id)
            
            order = Order.objects.create(customer=customer) 

            cart_items = CartItem.objects\
                .select_related('product')\
                .filter(cart_id=cart_id)
            
            order_items = [
                OrderItem(
                    order=order, 
                    product=item.product,
                    unit_price=item.product.unit_price,
                    quantity=item.quantity
                ) for item in cart_items
            ]

            OrderItem.objects.bulk_create(order_items)

            Cart.objects.filter(pk=cart_id).delete()

            order_created.send_robust(self.__class__, order=order)

            return order
        
class UpdateOrderSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Order
        fields = ['payment_status']