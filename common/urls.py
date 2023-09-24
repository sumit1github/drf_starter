from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('sign_up', views.SignupApi.as_view(),),
    path('login', views.Login.as_view(),),
    path('logout', views.LogOut.as_view(),)

]