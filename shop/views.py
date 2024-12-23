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