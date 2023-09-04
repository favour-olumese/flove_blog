from django.urls import path, include
from . import views
from django.contrib.auth.decorators import login_required

# app_name=
urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_user, name='register'),
    path('articles/', views.ArticleListView.as_view(), name='articles'),
    path('articles/search/', views.search, name='search'),
    path('article/create/', views.ArticleCreateView.as_view(), name='new-article'),
    path('@<str:username>/', views.WriterDetailView.as_view(), name='writer'),
    path('@<str:username>/delete', views.UserDeleteView.as_view(), name='delete-account'),
    path('@<str:username>/profile/update/', views.WriterUpdateView.as_view(), name='writer-profile-update'),
    path('@<str:username>/<slug:article_url>/', views.ArticleDetailView.as_view(), name='article-detail'),
    path('@<str:username>/<slug:article_url>/comment/', views.comment, name='article-comments'),
    path('@<str:username>/<slug:article_url>/comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name='delete-comment'),
    path('@<str:username>/<slug:article_url>/comment/reply/', views.reply, name='article-comments-replies'),
    path('@<str:username>/<slug:article_url>/comment/reply/<int:pk>/delete/', views.ReplyDeleteView.as_view(), name='delete-reply'),
    path('@<str:username>/<slug:article_url>/update/', views.ArticleUpdateView.as_view(), name='update-article'),
    path('@<str:username>/<slug:article_url>/delete/', views.ArticleDeleteView.as_view(), name='delete-article'),
    path('@<str:username>/<slug:article_url>/like/', views.article_likes, name='like-article'),
    path('@<str:username>/<slug:article_url>/save/', views.save_article, name='save-article'),
    path('me/articles/filter/', views.article_filter, name='filter'),
    path('me/articles/saved/', login_required(views.ArticleListView.as_view()), name='saved-articles'),
    path('writer/create/', views.WriterCreateView.as_view(), name='new-writer'),
]