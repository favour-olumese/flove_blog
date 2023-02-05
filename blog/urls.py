from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
]