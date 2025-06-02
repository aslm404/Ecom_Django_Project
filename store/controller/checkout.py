from django.shortcuts import render, redirect
from django.contrib import messages
from store.models import Product, Cart, Profile, Order, Orderitem
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import random

@login_required(login_url='store:loginpage')
def index(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product_qty > item.product.quantity:
            item.delete()
    total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
    return render(request, 'store/checkout.html', {'cartitem': cart_items, 'total_price': total_price})

@login_required(login_url='store:loginpage')
def placeorder(request):
    if request.method == 'POST':
        user = request.user

        required_fields = ['firstname', 'lastname', 'email', 'phone', 'address', 'city', 'state', 'country', 'pincode', 'payment_mode']
        missing_fields = [field for field in required_fields if not request.POST.get(field)]

        if missing_fields:
            error_message = f"Missing fields: {', '.join(missing_fields)}"
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': error_message}, status=400)
            
            messages.error(request, error_message)
            return redirect('store:checkout')



        # Update user name if not set
        if not user.first_name:
            user.first_name = request.POST.get('firstname', '')
            user.last_name = request.POST.get('lastname', '')
            user.save()

        # Create profile if it doesn't exist
        if not Profile.objects.filter(user=user).exists():
            Profile.objects.create(
                user=user,
                phone=request.POST.get('phone', ''),
                address=request.POST.get('address', ''),
                city=request.POST.get('city', ''),
                state=request.POST.get('state', ''),
                country=request.POST.get('country', ''),
                pincode=request.POST.get('pincode', '')
            )

        cart_items = Cart.objects.filter(user=user)
        total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)

        order = Order.objects.create(
            user=user,
            fname=request.POST.get('firstname', ''),
            lname=request.POST.get('lastname', ''),
            email=request.POST.get('email', ''),
            phone=request.POST.get('phone', ''),
            address=request.POST.get('address', ''),
            city=request.POST.get('city', ''),
            state=request.POST.get('state', ''),
            country=request.POST.get('country', ''),
            pincode=request.POST.get('pincode', ''),
            total_price=total_price,
            payment_mode=request.POST.get('payment_mode', ''),
            payment_id=request.POST.get('payment_id', '')
        )

        # Generate unique tracking number
        while True:
            tracking_no = 'Electrolyze' + str(random.randint(1111111, 9999999))
            if not Order.objects.filter(tracking_no=tracking_no).exists():
                break
        order.tracking_no = tracking_no
        order.save()

        # Create OrderItems & update stock
        for item in cart_items:
            Orderitem.objects.create(
                order=order,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )
            item.product.quantity -= item.product_qty
            item.product.save()

        # Clear the cart
        cart_items.delete()

        # Response for Razorpay
        if order.payment_mode == "Paid by Razorpay":
            return JsonResponse({'status': 'Your order has been placed successfully'})

        # For COD or other modes
        messages.success(request, "Order placed successfully!")
        return redirect('store:order')  # Ensure 'orders' is defined in urls.py

    return redirect('store:checkout')

@login_required(login_url='store:loginpage')
def razorpaycheck(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
    return JsonResponse({'total_price': total_price})
