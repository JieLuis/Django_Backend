from django.urls import path
from rest_framework.routers import SimpleRouter 
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')
router.register('collections', views.CollectionViewSet)
router.register('carts', views.CartViewSet)
router.register('customers', views.CustomerViewSet)
router.register('orders', views.OrderViewSet, basename='orders')

products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')
products_router.register('images', views.ProductImageViewSet, basename='product-images')

carts_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
carts_router.register('items', views.CartItemViewSet, basename='cart-items')


urlpatterns = router.urls + products_router.urls + carts_router.urls 
# URLConf 
# urlpatterns = [ 
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:id>/', views.ProductDetail.as_view())
# ]

