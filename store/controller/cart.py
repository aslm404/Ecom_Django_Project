from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from store.models import Product, Cart
from django.views.decorators.http import require_POST

@login_required(login_url='store:loginpage')
@require_POST
def addtocart(request):
    try:
        prod_id = int(request.POST.get('product_id'))
        prod_qty = int(request.POST.get('product_qty'))
        if prod_qty <= 0:
            return JsonResponse({'status': 'Quantity must be greater than 0'})
        
        product = get_object_or_404(Product, id=prod_id)
    except (TypeError, ValueError):
        return JsonResponse({'status': 'Invalid input data'})

    # Check if product already in cart
    if Cart.objects.filter(user=request.user, product=product).exists():
        return JsonResponse({'status': 'Product already in cart'})

    # Stock check
    if product.quantity < prod_qty:
        return JsonResponse({'status': f'Only {product.quantity} in stock'})

    # Add to cart
    Cart.objects.create(user=request.user, product=product, product_qty=prod_qty)
    return JsonResponse({'status': 'Product added successfully'})



@login_required(login_url='store:loginpage')
def viewcart(request):
    cart = Cart.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart': cart})

@require_POST
@login_required
def update_cart(request):
    prod_id = request.POST.get('product_id')
    prod_qty = request.POST.get('product_qty')
    
    try:
        prod_qty = int(prod_qty)
        cart_item = Cart.objects.get(user=request.user, product_id=prod_id)
        product = cart_item.product

        if prod_qty > product.quantity:
            return JsonResponse({'status': f'Only {product.quantity} in stock'})

        cart_item.product_qty = prod_qty
        cart_item.save()
        return JsonResponse({'status': 'Quantity updated successfully'})
    
    except Exception as e:
        return JsonResponse({'status': f'Error: {str(e)}'})


@login_required(login_url='store:loginpage')
def deletecartitem(request):
    if request.method == 'POST':
        try:
            prod_id = int(request.POST.get('product_id'))
            cart_item = Cart.objects.get(user=request.user, product_id=prod_id)
        except (TypeError, ValueError, Cart.DoesNotExist):
            return JsonResponse({'status': 'Cart item not found!'})

        cart_item.delete()
        return JsonResponse({'status': 'Item deleted successfully'})

    return redirect('/')
