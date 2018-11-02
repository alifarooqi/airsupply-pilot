from django.urls import path, re_path
from . import views

app_name = 'music'

urlpatterns = [
    #/order/
    path('', views.browse, name='browse'),
]
