from django.urls import path, include
from . import views

# app_name=
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('article/create/', views.ArticleCreateView.as_view(), name='new-article'),
    path('@<str:username>/', views.WriterDetailView.as_view(), name='writer'),
    path('@<str:username>/<slug:article_url>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('@<str:username>/<slug:article_url>/update/', views.ArticleUpdateView.as_view(), name='update-article'),
    path('@<str:username>/<slug:article_url>/delete/', views.ArticleDeleteView.as_view(), name='delete-article'),
    path('me/articles/', views.MyArticleListView.as_view(), name='my-articles'),
    path('me/articles/filter/', views.article_filter, name='filter'),
    path('me/drafts/', views.ArticleDraftListView.as_view(), name='drafts'),
    path('writer/create/', views.WriterCreateView.as_view(), name='new-writer'),
]