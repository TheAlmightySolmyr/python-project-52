from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views

urlpatterns = [
    path('', views.UserView.as_view(), name='user_list'),
    path('create/', views.UserCreate.as_view(), name='create'),
    path('<int:pk>/update/', views.UserUpdate.as_view(), name='update'),
    path('<int:pk>/delete/', views.UserDelete.as_view(), name='delete'),
]