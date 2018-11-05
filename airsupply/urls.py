from django.urls import path, re_path
from . import views


urlpatterns = [
    #/
    path('browse/', views.browse, name='browse'),

]
