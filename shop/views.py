from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products' 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    # context_object_name　これ何かよくわかってない
    context_object_name = 'product'