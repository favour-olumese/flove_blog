from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Writer, Article

# admin.site.register(User, UserAdmin)

admin.site.register(Writer)

class ArticleAdmin(admin.ModelAdmin):
    fields = ['writer', 'title', 'text', 'article_img', 'pub_date', 'update_date']
    readonly_fields = ['pub_date', 'update_date']  # For non-editable fields

admin.site.register(Article, ArticleAdmin)