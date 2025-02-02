from django.urls import path
from . import views

app_name = 'promotion'

urlpatterns = [
    path('apply/', views.apply_promotion_code, name='apply_promotion_code'),
    path('remove/', views.remove_promotion_code, name='remove_promotion_code'),
] 