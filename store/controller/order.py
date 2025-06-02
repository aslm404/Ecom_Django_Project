from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from store.models import Order, Orderitem

@login_required(login_url='store:loginpage')
def order_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, "store/order.html", {'orders': orders})

@login_required(login_url='store:loginpage')
def view_order(request, t_no):
    order = get_object_or_404(Order, tracking_no=t_no, user=request.user)
    order_items = Orderitem.objects.filter(order=order)
    return render(request, "store/orderitem.html", {'order': order, 'orderitem': order_items})
