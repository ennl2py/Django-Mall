from django.db import models


class CartInfo(models.Model):
    user = models.ForeignKey('user_part.Userinfo', on_delete=models.CASCADE)
    product = models.ForeignKey('products.ProductInfo', on_delete=models.CASCADE)
    count = models.IntegerField()
