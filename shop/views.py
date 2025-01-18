from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Product
from .forms import ProductForm
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from basicauth.decorators import basic_auth_required

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

    # ここ、django_tutorialでQuerySetってやつ使ってたからそれ調べる。
    # get_context_data メソッドのオーバーライド
    # DetailView はもともとテンプレートに必要なデータ（product）をコンテキストに渡している
    # このメソッドを拡張することで、既存のcontextを維持しながら新しい'latest_products_list'を追加できる
    # super().get_context_data(**kwargs) を使うことで、元のコンテキスト（productなど）を保持しつつ、データを追加できる
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_products_list'] = Product.objects.order_by("-created_at")[:5]
        print(context)  # 確認
        return context


@method_decorator(basic_auth_required, name='dispatch')
class AdminProductListView(ListView):
    model = Product
    template_name = 'shop/admin_products_list.html'
    context_object_name = 'products'

@method_decorator(basic_auth_required, name='dispatch')
class AdminProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/admin_product_form.html'
    success_url = reverse_lazy('admin_products_list')

@method_decorator(basic_auth_required, name='dispatch')
class AdminProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'shop/admin_product_form.html'
    success_url = reverse_lazy('admin_products_list')

@method_decorator(basic_auth_required, name='dispatch')
class AdminProductDeleteView(DeleteView):
    model = Product
    template_name = 'shop/admin_product_confirm_delete.html'
    success_url = reverse_lazy('admin_products_list')