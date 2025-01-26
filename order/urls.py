from django.urls import path
from . import views

app_name = 'order'

urlpatterns = [
    path('', views.purchase, name='purchase'),
    path('list/', views.OrderListView.as_view(), name='order_list'),
    path('detail/<int:pk>/', views.OrderDetailView.as_view(), name='order_detail'),
]
