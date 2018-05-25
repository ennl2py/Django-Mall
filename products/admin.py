from django.contrib import admin
from products.models import ProductType, ProductInfo


class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_name']


class ProductInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'product_name', 'product_price', 'product_click', 'product_unit',
                    'product_stock', 'product_type']


admin.site.register(ProductType, ProductTypeAdmin)
admin.site.register(ProductInfo, ProductInfoAdmin)
