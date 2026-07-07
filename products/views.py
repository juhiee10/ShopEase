from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Product


@login_required
def product_list(request):
    products = Product.objects.all()

    return render(request, "products/products.html", {
        "products": products
    })


@login_required
def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    return render(request, "products/product_detail.html", {
        "product": product
    })