from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions, IsAdminUser
from rest_framework.viewsets import ModelViewSet, GenericViewSet 
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from store.permission import FullDjangoPermissions, IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Order, Product, OrderItem, ProductImage, Review, Customer
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductImageSerializer, ProductSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    pagination_class = DefaultPagination
    search_fields = ['title', 'description']
    ordering_fields = ['unit_price', 'last_update']
    permission_classes = [IsAdminOrReadOnly]

    # def get_queryset(self):
    #     qeuryset = Product.objects.all()
    #     collection_id = self.request.query_params.get('collection_id')
    #     if collection_id is not None:
    #         return qeuryset.filter(collection_id = collection_id )
    #     return qeuryset
 
    def get_serializer_context(self):  
        return {'request' : self.request}
    
    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Product cannot be deleted becasue item exist'})
        
        return super().destroy(request, *args, **kwargs)
    
###########################################################
 #### ^^^^^^^^^^^^^combine ProductDetail to the class above #########
# class ProductList(ListCreateAPIView):
#     queryset = Product.objects.select_related('collection').all()
#     serializer_class = ProductSerializer
    
#     def get_serializer_context(self):
#         return {'request' : self.request}
###########################################################
    

    ###########################################################
    #### ^^^^^^^^^^^^^evolve to the method above #########
    # def get_queryset(self):
    #     return Product.objects.select_related('collection').all()
    
    # def get_serializer_class(self):
    #     return ProductSerializer
    
    # def get_serializer_context(self):
    #     return {'request' : self.request}
    ###########################################################



    ###########################################################
    #### ^^^^^^^^^^^^^evolve to the method above #########
    # def get(self, request: HttpRequest):
    #     qeuryset = Product.objects.select_related('collection').all()
    #     serializer = ProductSerializer(qeuryset, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request):
    #     serializer = ProductSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     serializer.save()
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)
    ###########################################################


    
###########################################################
#### ^^^^^^^^^^^^^combine ProductList to ModelViewSet #########    
# class ProductDetail(APIView):
#     def get(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product)
#         return  Response(serializer.data)
    
#     def put(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         serializer = ProductSerializer(product, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
#     def delete(self, request, id):
#         product = get_object_or_404(Product, pk=id)
#         if product.orderitems.count() > 0:
#             return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
#         product.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
###########################################################

    
class ReviewViewSet(ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin, RetrieveModelMixin,  DestroyModelMixin, GenericViewSet ):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']
    def get_serializer_class(self):
        if self.request.method == "POST":
            return AddCartItemSerializer
        elif self.request.method == "PATCH":
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart_id=self.kwargs['cart_pk']) \
        .select_related('product')
    
    def get_serializer_context(self):
        return {'cart_id' : self.kwargs['cart_pk']}
    

class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [FullDjangoPermissions]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission])
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        (customer, createdOrNot) = Customer.objects.get_or_create(user_id = request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
    #  return Response(request.user.id)

class OrderViewSet(ModelViewSet):
    http_method_names = ['get', 'patch', 'delete', 'head', 'options', 'post ']
    def get_permissions(self):
        if self.request.method in ['PUT','PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        user_id = self.request.user.id

        serializer = CreateOrderSerializer(data=request.data,
            context={'user_id' : user_id}
        )  

        serializer.is_valid(raise_exception=True)
        order = serializer.save() 
        
        serializer = OrderSerializer(order)
        return Response(serializer.data) 

    def get_serializer_class(self):
       if self.request.method == 'POST':
        return CreateOrderSerializer
       elif self.request.method == 'PATCH':
        return UpdateOrderSerializer
       return OrderSerializer 
    
    def get_serializer_context(self):
        return {'user_id' : self.request.user.id}
    
    def get_queryset(self):
        user = self.request.user

        if user.is_staff:
            return Order.objects.prefetch_related('items').all()
        
        (customer_id, createdOrNot) = Customer\
            .objects.only('id')\
            .get(user_id = user.id)
        
        return Order.objects.filter(customer= customer_id)

class ProductImageViewSet(ModelViewSet):
    serializer_class = ProductImageSerializer
    
    def get_queryset(self):
        return ProductImage.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}