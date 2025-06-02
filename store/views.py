from django.shortcuts import render, get_object_or_404
from .models import Category, Product

def home(request):
    trending_products = Product.objects.filter(trending=True, status=False)[:12]
    context = {'trending_products': trending_products}
    return render(request, "store/index.html", context)

def collections(request):
    categories = Category.objects.filter(status=False)
    context = {'categories': categories}
    return render(request, 'store/collections.html', context)

def collectionsview(request, slug):
    category = get_object_or_404(Category, slug=slug, status=False)
    products = Product.objects.filter(category=category, status=False)
    context = {'products': products, 'category_name': category}
    return render(request, 'store/products/home.html', context)

def productview(request, cate_slug, prod_slug):
    category = get_object_or_404(Category, slug=cate_slug, status=False)
    product = get_object_or_404(Product, category=category, slug=prod_slug, status=False)
    context = {'product': product}
    return render(request, "store/products/view.html", context)

def search(request): 
    if request.method == "GET":
        query = request.GET.get('search')
        if query and len(query) >= 2:
           
            products = Product.objects.filter(name__icontains=query)
            
            context = {'products': products, 'query': query}
            return render(request, 'store/search_result.html', context)
        else:
            # Handle case where the query is too short
            msg = "Please enter at least 2 characters for your search query."
            return render(request, 'store/search_result.html', {'msg': msg})

    # Default render for GET requests without a search query
    return render(request, 'store/search_result.html')