from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),    #  store/
    path('<int:product_id>', views.product_detail, name='product_detail'), # store/1
    path('order/<int:product_id>', views.order_views, name='order_views'), # store/order/1
    path('orders', views.order_list, name='order_list'), # store/orders
]