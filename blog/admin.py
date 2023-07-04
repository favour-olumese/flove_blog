from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Writer, Article, Comment, Reply

# admin.site.register(User, UserAdmin)


class WriterAdmin(admin.ModelAdmin):
    """Adds the Writer model to the admin dashboard."""

    fields = ['user', 'first_name', 'last_name', 'profile_picture',
    'bio', 'display_email', 'website_url', 'linkedin_url', 'saved_articles']

    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     if db_field.name == 'saved_articles':
    #         kwargs["queryset"] = Article.objects.saved_articles
    #     return super(Writer, self).formfield_for_manytomany(db_field, request, **kwargs)


admin.site.register(Writer)


class ArticleAdmin(admin.ModelAdmin):
    """Adds the Article model to the admin dashboard."""

    fields = ['writer', 'title', 'text', 'article_img', 'pub_date', 
    'update_date', 'article_url', 'article_audio', 'article_status', 'likes']
    
    # Non-editable fields
    readonly_fields = ['pub_date', 'update_date', 'article_url', 'article_audio']




admin.site.register(Article, ArticleAdmin)


class CommentAdmin(admin.ModelAdmin):
    """Adds the Comment model to the admin dashboard."""

    fields = ['commenter', 'text', 'article', 'date']
    
    # Non-editable fields
    readonly_fields = ['date']


admin.site.register(Comment, CommentAdmin)


class ReplyAdmin(admin.ModelAdmin):
    """Adds the Reply model to the admin dashboard."""
    fields = ['replier', 'reply_text', 'article', 'comment', 'date']
    
    # Non-editable fields
    readonly_fields = ['date']


admin.site.register(Reply, ReplyAdmin)