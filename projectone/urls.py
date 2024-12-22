"""
URL configuration for projectone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from store import views
from store.controller import authview,cart,wishlist,checkout,order
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('store/',include('store.urls')),
    path('',views.home,name='home'),

    path('register/',authview.register,name='register'),
    path('login/',authview.loginpage,name='loginpage'),
    path('logout/',authview.logoutpage,name='logoutpage'),



    path('add-to-cart', cart.addtocart, name='add-to-cart'),
    path('cart', cart.viewcart, name='cart'),
    path('update-cart', cart.updatecart, name='update_cart'),
    path('delete-cart-item', cart.deletecartitem, name='delete-cart-item'),
    path('wishlist', wishlist.index, name='wishlist'),

    path('checkout', checkout.index, name='checkout'),
    path('place-order', checkout.placeorder, name='placeorder'),

    path('order/',order.order_view,name='order'),
    path('view-order/<str:t_no>/',order.view_order,name='orderview')








]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)