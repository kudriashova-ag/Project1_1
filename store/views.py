from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt

from store.models.attribute import AttributeValue
from store.models.tag import Tag
from .models import Product, Category
from django.shortcuts import render, get_object_or_404


# View функціі
def home(request):
    totalProducts = Product.objects.count()
    available_products = Product.objects.filter(is_available=True, stock__gt=0).count()
    latest_products = Product.objects.filter(is_available=True, stock__gt=0).order_by('-created_at')[:4]
    
    context = {
        'totalProducts': totalProducts,
        'available_products': available_products,
        'latest_products': latest_products,
        'heading': '<i>My Store</i>'
        }
    return render(request, "store/home.html", context)


def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/category.html', {
        'category': category,
        'products': products
    })


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'store/product_list.html', {
        'category': category,
        'categories': categories,
        'products': products,
    })


def product_detail(request, product_slug):
    product = get_object_or_404(Product, slug=product_slug)
    
    attributes = AttributeValue.objects.filter(
        products__product=product
    ).select_related('attribute')
    
    tags = Tag.objects.filter(
        producttag__product=product
    )
    
    return render(request, 'store/product_detail.html', {
        'product': product,
        'attributes': attributes,
        'tags': tags,
    })


@csrf_exempt
def order_views(request, product_id):
    pass
    

def order_list(request):
   pass

    
def search(request):
    pass