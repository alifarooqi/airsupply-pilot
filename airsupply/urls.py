from django.urls import path, re_path
from . import views

app_name = 'airsupply'

urlpatterns = [

    #users
    re_path(r'^$', views.UserLoginView.as_view(), name='login'),
    re_path(r'^logout/$', views.logout_user, name='logout'),
    path('account/', views.UserAccount.as_view(), name='account'),
    re_path(r'^register/(?P<usernameb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.UserRegisterView.as_view(), name='register'),
    re_path(r'^register/$', views.UserRegisterView.as_view(), name='confirm_registration'),
    re_path(r'^forgot_password/$', views.UserForgotPassword.as_view(), name='forgot_password'),

    #clinic manager
    path('browse/', views.BrowseView.as_view(), name='browse'),
    re_path(r'browse/(?P<catID>[0-9]+)/$', views.BrowseView.as_view(), name='browse_cat'),
    path('cart/', views.CartView.as_view(),  name='cart'),
    path('my_orders/', views.OrderView.as_view(), name='my_orders'),
    re_path(r'my_orders/cancel/(?P<pk>[0-9]+)/$', views.cancelOrder, name='cancel_order'),
    re_path(r'my_orders/receive/(?P<pk>[0-9]+)/$', views.receiveOrder, name='receive_order'),
    path('cart/add/', views.cart_add, name='cart_add'),  # Change main.js too if URL is changed
    path('cart/checkout/', views.cart_checkout, name='cart_checkout'),
    re_path(r'order/(?P<pk>[0-9]+)/$', views.OrderDetailView.as_view(), name='view_order_details'),
    re_path(r'remove_item/(?P<order_pk>[0-9]+)/(?P<item_pk>[0-9]+)/$', views.delete_item, name='remove_item'),

    #dispatcher
    path('dispatch/', views.DispatchView.as_view(), name='dispatch_view'),
    re_path(r'dispatch/itinerary/(?P<pk>[0-9]+)/$', views.get_itinerary, name='get_itinerary'),
    re_path(r'dispatch/(?P<pk>[0-9]+)/$', views.dispatch, name='dispatch_drone'),

    #warehouse personnel
    re_path(r'priority_queue/$', views.PriorityQueueView.as_view(), name='priority_queue'),
    re_path(r'priority_queue/1/(?P<pk>[0-9]+)/$', views.processing_order, name='order_processing'),
    re_path(r'priority_queue/2/(?P<pk>[0-9]+)/$', views.order_processed, name='order_processed'),
    re_path(r'priority_queue/3/(?P<pk>[0-9]+)/$', views.download_shipping, name='download_shipping'),

]
