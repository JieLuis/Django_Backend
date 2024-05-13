from django.urls import path
from rest_framework.routers import SimpleRouter 
from rest_framework_nested import routers
from . import views

router = routers.DefaultRouter()
router.register('products', views.ProductViewSet, basename='products')


products_router = routers.NestedDefaultRouter(router, 'products', lookup = 'product')
products_router.register('reviews', views.ReviewViewSet, basename = 'product-reviews')

urlpatterns = router.urls + products_router.urls
# URLConf 
# urlpatterns = [ 
#     path('products/', views.ProductList.as_view()),
#     path('products/<int:id>/', views.ProductDetail.as_view())
# ]

