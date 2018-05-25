from django.db import models
from tinymce.models import HTMLField


class ProductType(models.Model):
    type_name = models.CharField(max_length=20)
    is_Delete = models.BooleanField(default=False)

    def __str__(self):
        return self.type_name


class ProductInfo(models.Model):
    product_name = models.CharField(max_length=30)
    product_img = models.ImageField(upload_to='product_img')
    product_price = models.DecimalField(max_digits=6, decimal_places=2)
    is_Delete = models.BooleanField(default=False)
    product_click = models.IntegerField(default=0)
    product_unit = models.CharField(max_length=20)
    product_abstract = models.CharField(max_length=120)
    product_stock = models.IntegerField()
    product_content = HTMLField()
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


