from django.contrib import admin
from . models import *




@admin.register(Product)
class ProductDisplay(admin.ModelAdmin):
    list_display = ('product_name', 'product_image', 'prduct_price')
    list_display_links = ('product_name', 'product_image', 'prduct_price')

@admin.register(Order)
class OrderDisplay(admin.ModelAdmin):
    list_display = ('product', 'instamojo_response', 'is_paid', 'order_id')
    list_display_links = ('product', 'instamojo_response', )
