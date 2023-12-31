
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

User = get_user_model()

class Order(models.Model):
    order_user = models.ForeignKey(verbose_name='사용자번호', to= User, on_delete=models.CASCADE, null=True, blank=True)
    order_price = models.DecimalField(verbose_name='가격', max_digits=10, decimal_places=2)
    order_request = models.CharField(verbose_name='요청사항', max_length=30, null=True)
    order_color = models.CharField(verbose_name='색상', max_length=2)
    order_date = models.DateTimeField(verbose_name='주문날짜', auto_now_add=True)
    print_date = models.CharField(verbose_name='프린트 날짜', max_length=30, null=True)

class OrderFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    file = models.FileField(upload_to='files/')