from django.shortcuts import render, redirect
from store.models import Product, Wishlist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='store:loginpage')
def index(request):
    wishlist = Wishlist.objects.filter(user=request.user)
    return render(request, 'store/wishlist.html', {'wishlist': wishlist})

def addtowishlist(request, product_id):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Login to continue!'})

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return JsonResponse({'status': 'No such product found!'})

        if Wishlist.objects.filter(user=request.user, product=product).exists():
            return JsonResponse({'status': 'Product is already in wishlist!'})

        Wishlist.objects.create(user=request.user, product=product)
        return JsonResponse({'status': 'Product added to wishlist!'})

    return redirect('/')


def deletewishlistitem(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({'status': 'Login to continue!'})

        try:
            prod_id = int(request.POST.get('product_id'))
            wishlist_item = Wishlist.objects.get(user=request.user, product_id=prod_id)
            wishlist_item.delete()
            return JsonResponse({'status': 'Product removed from wishlist!'})
        except (ValueError, Wishlist.DoesNotExist):
            return JsonResponse({'status': 'Product not found in wishlist!'})

    return redirect('/')
