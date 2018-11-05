from django.urls import path, re_path
from . import views


urlpatterns = [
    #/main/browse/
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('my_orders/', views.OrderView.as_view(), name='my_orders'),
]
