from django.urls import path, re_path
from . import views

app_name = 'airsupply'

urlpatterns = [

    #clinic manager
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('my_orders/', views.OrderView.as_view(), name='my_orders'),
    path('cart/add/', views.cart_add, name='cart_add'),  # Change main.js too if URL is changed
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    re_path(r'order/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='view_order_details'),

    #dispatcher
    path('dispatch/', views.DispatchView.as_view(), name='dispatch_view'),
    re_path(r'dispatch/itinerary/(?P<pk>[0-9]+)/$', views.get_itinerary, name='get_itinerary'),
    re_path(r'dispatch/(?P<pk>[0-9]+)/$', views.dispatch, name='dispatch_drone'),

    #warehouse personnel
    re_path(r'priority_queue/$', views.PriorityQueueView.as_view(), name='priority_queue'),
    re_path(r'priority_queue/(?P<pk>[0-9]+)/$', views.order_processed, name='order_processed'),

]
