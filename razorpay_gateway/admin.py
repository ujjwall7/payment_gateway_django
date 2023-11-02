from django.contrib import admin
from . models import Coffee


@admin.register(Coffee)
class CoffeeDisplay(admin.ModelAdmin):
    list_display = ('name', 'amount', 'order_id', 'email', 'paid', )
