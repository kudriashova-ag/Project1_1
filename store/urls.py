from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),    #  store/
    path('category/<slug:category_slug>/', views.category, name='category'),
    path('product/<slug:product_slug>', views.product_detail, name='product_detail'), # store/1
    
    path('order/<int:product_id>', views.order_views, name='order_views'), # store/order/1
    path('orders', views.order_list, name='order_list'), # store/orders
    path('search', views.search, name='search'),
]