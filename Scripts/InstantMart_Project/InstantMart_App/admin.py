from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['id','category_name','category_img']

@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    list_display=['unit_name']

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display=['currency_symbol']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display=['product_name','category','product_img','product_quantity','product_unit','product_currency','product_price']
    list_filter=['category']

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display=['id','product','user','quantity','subtotalprice']