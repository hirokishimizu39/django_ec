from django.urls import path
from . import views

app_name = 'promotion'

urlpatterns = [
    path('apply/', views.apply_promotion_code, name='apply_promotion_code'),
] 