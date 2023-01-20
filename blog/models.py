from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class BlogUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='user_img', null=True, blank=True)

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class Articles(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    ) # https://docs.djangoproject.com/en/4.1/topics/auth/customizing/#referencing-the-user-model
    title = models.CharField(max_length=100)
    text = models.TextField()
    article_img = models.ImageField(upload_to='article_img', null=True, blank=True)
    # article_tag = models.CharField(max_length=100)

    def __str__(self):
        return self.title


class Comments(models.Model):
    pass