from django.urls import path
from . import views
from store.controller import authview, cart, wishlist, checkout, order
from django.conf import settings
from django.conf.urls.static import static

app_name = 'store'

urlpatterns = [
    # General Store Pages
    path('', views.home, name='home'),
    path('collections/', views.collections, name='collections'),
    path('collections/<slug:slug>/', views.collectionsview, name='collectionsview'),
    path('collections/<slug:cate_slug>/<slug:prod_slug>/', views.productview, name='productview'),
    path('search/', views.search, name='search_result'),

    # Authentication
    path('register/', authview.register, name='register'),
    path('login/', authview.loginpage, name='loginpage'),
    path('logout/', authview.logoutpage, name='logoutpage'),

    # Cart URLs
    path('add-to-cart/', cart.addtocart, name='add_to_cart'),
    path('cart/', cart.viewcart, name='cart'),
    path('update-cart/', cart.update_cart, name='update_cart'),
    path('delete-cart-item/', cart.deletecartitem, name='delete_cart_item'),

    # Wishlist URLs
    path('wishlist/', wishlist.index, name='wishlist'),
    path('add-to-wishlist/<int:product_id>/', wishlist.addtowishlist, name='add_to_wishlist'),
    path('delete-wishlist-item/', wishlist.deletewishlistitem, name='delete_wishlist_item'),

    # Checkout and Order
    path('checkout/', checkout.index, name='checkout'),
    path('place-order/', checkout.placeorder, name='placeorder'),
    path('proceed-to-pay/', checkout.razorpaycheck, name='proceed_to_pay'),

    # Order Views
    path('order/', order.order_view, name='order'),
    path('view-order/<str:t_no>/', order.view_order, name='orderview'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
