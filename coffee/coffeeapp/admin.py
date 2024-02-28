from django.contrib import admin
from . models import Product,Cart,Order

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display=['id','name','price','pdetails','category','is_active']
    list_filter=['category','is_active']


admin.site.register(Product,ProductAdmin)
admin.site.register(Cart)
admin.site.register(Order)