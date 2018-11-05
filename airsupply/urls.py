from django.urls import path, re_path
from . import views


urlpatterns = [
    #/main/login/
    path('login/', views.login, name='login'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('browse/', views.BrowseView.as_view(), name='browse'),
    path('cart/', views.CartView.as_view(), name='cart'),
    path('my_orders/', views.OrderView.as_view(), name='my_orders'),
]
