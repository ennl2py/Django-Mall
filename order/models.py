from django.db import models


class OrderInfo(models.Model):
    order_id = models.CharField(max_length=20, primary_key=True)
    order_user = models.ForeignKey('user_part.UserInfo', on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now=True)
    is_Pay = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    address = models.CharField(max_length=140)


class OrderDetailInfo(models.Model):
    products = models.ForeignKey('products.ProductInfo', on_delete=models.CASCADE)
    order = models.ForeignKey(OrderInfo, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    count = models.IntegerField()