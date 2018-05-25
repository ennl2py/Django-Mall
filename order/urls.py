from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.order),
    url(r'^order_handler/$', views.order_handler),
    url(r'^pay/(\d+)$', views.pay)
]