from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.loginPage, name='loginpage'),
    path("logout/", views.logoutPage, name='logoutpage'),
    path("register/", views.registerUser, name='register'),

    path('', views.home, name="home"),
    path('room/<str:pk>/', views.room, name='room'),
    path('createform/', views.cform, name='new'),
    path('update/<str:pk>/', views.update, name='update'),
    path('delete/<str:pk>/', views.delete, name='delete')



]