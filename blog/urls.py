from django.urls import path, include
from . import views
from django_email_verification import urls as email_urls


urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('email/', include(email_urls), name='email-verification'),
]