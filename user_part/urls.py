from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^register/$', views.register),
    url(r'^register_handler/$', views.register_handler),
    url(r'^register_judge/$', views.register_judge),
    url(r'^login/$', views.login),
    url(r'^login_judge/$', views.login_judge),
    url(r'^login_handler/$', views.login_handler),
    url(r'^forget/$', views.forget),
    url(r'^reset/$', views.reset),
    url(r'^logout/$', views.logout),
    url(r'^info/$', views.info),
    url(r'^order/$', views.order),
    url(r'^order/(\d+)$', views.order_page),
    url(r'^site/$', views.site),
]
