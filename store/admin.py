from django.contrib import admin
from .models import Category, Product, Cart, Wishlist, Order, Orderitem, Profile

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'slug', 'status', 'trending']
    search_fields = ['name', 'slug']
    list_filter = ['status', 'trending']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'selling_price', 'quantity', 'status', 'trending']
    search_fields = ['name', 'slug', 'tag']
    list_filter = ['category', 'status', 'trending']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'product_qty', 'created_at']
    search_fields = ['user__username', 'product__name']
    list_filter = ['created_at']

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'product', 'created_at']
    search_fields = ['user__username', 'product__name']
    list_filter = ['created_at']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'tracking_no', 'status', 'payment_mode', 'created_at']
    search_fields = ['user__username', 'tracking_no', 'phone']
    list_filter = ['status', 'created_at']

@admin.register(Orderitem)
class OrderitemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']
    search_fields = ['order__tracking_no', 'product__name']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'city', 'country', 'created_at']
    search_fields = ['user__username', 'phone', 'city']
