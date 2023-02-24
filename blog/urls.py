from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('myarticles/', views.MyArticleListView.as_view(), name='my-articles'),
    path('myarticles/filter/', views.article_filter, name='filter'),
    path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    path('article/create', views.ArticleCreateView.as_view(), name='new-article'),
    path('article/<int:pk>/update', views.ArticleUpdateView.as_view(), name='update-article'),
    path('article/<int:pk>/delete', views.ArticleDeleteView.as_view(), name='delete-article'),
    path('me/drafts/', views.ArticleDraftListView.as_view(), name='drafts'),
    path('writer/create', views.WriterCreateView.as_view(), name='new-writer'),
    path('@<str:username>', views.WriterDetailView.as_view(), name='writer'),
    path('register/', views.register_user, name='register'),
]