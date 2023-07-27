from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse


class Writer(models.Model):
    """Class containing writer's information."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    profile_picture = models.ImageField(upload_to='img/user_img/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    display_email = models.BooleanField(default=False)
    website_url = models.URLField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    saved_articles = models.ManyToManyField("Article", related_name='saved_articles', blank=True)

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns url of each writer."""

        return reverse('writer', kwargs={'username':self.user})

    def __str__(self):
        """Returns writer's name."""

        return f'{self.last_name} {self.first_name}'


class Article(models.Model):
    """Class for articles."""

    # Choices to make articles either draft, public, or unlisted.
    ARTICLE_STATUS = (
        ('d', 'Draft'),
        ('p', 'Public'),
        ('u', 'Unlisted'),
    )

    # Choices for writer to have article audio displayed on article detail page.
    DISPLAY_AUDIO = (
        ('y', 'Yes'),
        ('n', 'No'),
    )

    writer = models.ForeignKey(Writer, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    text = models.TextField()
    article_img = models.ImageField(upload_to='img/article_img/', null=True, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True) 
    update_date = models.DateTimeField(auto_now=True)
    article_status = models.CharField(max_length=1, choices=ARTICLE_STATUS, default='d')
    article_url = models.CharField(max_length=120)
    article_audio = models.FileField(upload_to='article_audio/')
    display_audio = models.CharField(max_length=1, choices=DISPLAY_AUDIO)
    likes = models.ManyToManyField(Writer, related_name='article_likes', blank=True)
    # article_tag = models.CharField(max_length=100)


    class Meta:
        ordering = ['-pub_date']

    def get_absolute_url(self):
        """Returns url of each article."""

        return reverse('article-detail', kwargs={'article_url':self.article_url, 'username':self.writer.user})

    def __str__(self):
        """Returns article title."""

        return f'{self.title} by {self.writer}'


class Comment(models.Model):
    """Class containing comments of writers."""

    text = models.TextField()
    commenter = models.ForeignKey(Writer, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        """String name"""

        return f'{self.commenter} comment in {self.article}'


# class Reply(models.Model):
#     """Class containing reply to comments of writers."""

#     text = models.TextField()
#     replier = models.ForeignKey(Writer, on_delete=models.CASCADE)
#     article = models.ForeignKey(Article, on_delete=models.CASCADE)
#     comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
#     date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         """String name"""

#         return f'{self.commenter} comment in {self.article}' 

class Reply(models.Model):
    """Class containing comments of writers."""

    reply_text = models.TextField()
    replier = models.ForeignKey(Writer, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)  # Comment replied to
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        """Returns string name"""

        return f'{self.replier} replied {self.comment}'
