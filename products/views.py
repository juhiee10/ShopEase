from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def product_list(request):
    return render(request, "products/products.html")

@login_required
def product_detail(request, id):
    return render(request, "products/product_detail.html")