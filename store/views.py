from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.response import Response 
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from .models import Product, OrderItem, Review
from .serializers import ProductSerializer, ReviewSerializer
class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

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
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    # def get_queryset(self):
    #     qeuryset = Product.objects.all()
    #     collection_id = self.request.query_params['collection_id']
    #     if collection_id is not None:
    #         return qeuryset.filter(collection_id = collection_id )
    #     return qeuryset

    def get_serializer_context(self):
        return {'product_id' : self.kwargs['product_id']}






