from django.urls import path, re_path
from . import views


urlpatterns = [
    #/main/browse/
    path('browse/', views.BrowseView.as_view(), name='browse'),

]
