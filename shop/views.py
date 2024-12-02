from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Product

# Create your views here.
class ProductListView(ListView):
    model = Product
    template_name = 'shop/index.html'
    # cotext_object_nameをproducts_listに指定することで、products_listにインスタンスを代入。インスタンス化のライブラリ的なもの products_list = Product.objects.all()を勝手にやってくれてる。
    # これによって、products_list.nameとかで引っ張って来れる
    context_object_name = 'products_list' 

class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'