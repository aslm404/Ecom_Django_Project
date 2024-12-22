from django.shortcuts import redirect, render
from django.contrib import messages
from store.models import Product, Cart, Profile, Order, Orderitem
from django.http.response import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import random


@login_required(login_url='loginpage')
def index(request):
    cart_items = Cart.objects.filter(user=request.user)
    for item in cart_items:
        if item.product_qty > item.product.quantity:
            item.delete()  # Correct deletion method

    total_price = sum(item.product.selling_price * item.product_qty for item in cart_items)
    context = {'cartitem': cart_items, 'total_price': total_price}
    return render(request, 'store/checkout.html', context)


@login_required(login_url='loginpage')
def placeorder(request):
    if request.method == 'POST':
        currentuser = User.objects.filter(id=request.user.id).first()

        if not currentuser.first_name:
            currentuser.first_name = request.POST.get('firstname')
            currentuser.last_name = request.POST.get('lastname')
            currentuser.save()

        if not Profile.objects.filter(user=request.user):
            userprofile = Profile()
            userprofile.user = request.user
            userprofile.phone = request.POST.get('phone')
            userprofile.address = request.POST.get('address')
            userprofile.city = request.POST.get('city')
            userprofile.state = request.POST.get('state')
            userprofile.country = request.POST.get('country')
            userprofile.pincode = request.POST.get('pincode')
            userprofile.save()

        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('firstname')
        neworder.lname = request.POST.get('lastname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.address = request.POST.get('address')
        neworder.city = request.POST.get('city')
        neworder.state = request.POST.get('state')
        neworder.country = request.POST.get('country')
        neworder.pincode = request.POST.get('pincode')

        neworder.payment_mode = request.POST.get('payment_mode')
        neworder.payment_id = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = sum(item.product.selling_price * item.product_qty for item in cart)

        neworder.total_price = cart_total_price
        trackno = 'Electrolyze' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno).exists():
            trackno = 'Electrolyze' + str(random.randint(1111111, 9999999))

        neworder.tracking_no = trackno
        neworder.save()

        for item in cart:
            Orderitem.objects.create(
                order=neworder,
                product=item.product,
                price=item.product.selling_price,
                quantity=item.product_qty
            )

            # Decrease the product quantity from available stock
            orderproduct = Product.objects.filter(id=item.product_id).first()
            orderproduct.quantity -= item.product_qty
            orderproduct.save()

        

        # messages.success(request, "Your order has been placed successfully")

        payMode = request.POST.get('payment_mode')
        if payMode == "Paid by Razorpay":
            return JsonResponse({'status': 'Your order has been placed successfully'})

        # Clear user cart
        Cart.objects.filter(user=request.user).delete()    
    return redirect('order/')

@login_required(login_url='loginpage')
def razorpaycheck(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart_items:
        total_price += item.product.selling_price * item.product_qty

    return JsonResponse({
        'total_price':total_price
    })    
