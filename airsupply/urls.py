from django.urls import path, re_path
from . import views

app_name = 'airsupply'

urlpatterns = [

    #clinic manager
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('my_orders/', views.OrderView.as_view(), name='my_orders'),
    path('cart/add/', views.cart_add, name='cart_add'),
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),

    #dispatcher
    path('dispatch/', views.DispatchView.as_view(), name='dispatch_view'),
    re_path(r'dispatch/(?P<pk>[0-9]+)/$', views.dispatch, name='dispatch_drone'),

]
