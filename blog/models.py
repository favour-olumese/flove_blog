from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Writer(models.Model):
    """Class containing writer's information."""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='user_img', null=True, blank=True)
    bio = models.TextField(null= True, blank=True)
    # TODO: Add field for links to social media pages.


    class Meta:
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Article(models.Model):
    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    article_img = models.ImageField(upload_to='article_img', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True) 
    update_date = models.DateTimeField(auto_now=True)
    # article_tag = models.CharField(max_length=100)


    class Meta:
        ordering = ['-update_date']


    def __str__(self):
        return f'{self.title} by {self.writer}'


class Comment(models.Model):
    pass