from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/create', views.ArticleCreateView.as_view(), name='new-article'),
    path('writer/create', views.WriterCreateView.as_view(), name='writer'),
    path('register/', views.register_user, name='register'),
]