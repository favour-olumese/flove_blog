from django.contrib.syndication.views import Feed
from blog.models import Writer, Article

class WriterFeed(Feed):
    description_template = 'feeds/beat_description.html'

    def get_object(self, request, username):
        """
        Takes the current request and the arguments from the URL, and
        returns an object represented by this feed.

        Raises django.core.exceptions.ObjectDoesNotExist on error.
        """
        return Writer.objects.get(user__username=username)
    
    def title(self, obj):
        """
        Takes the object returned by get_object() and returns the
        feed's title as a normal Python string.
        """
        return "Articles by %s on Flove." % obj
    
    def link(self, obj):
        """
        Takes the object returned by get_object() and returns the URL
        of the HTML version of the feed as a normal Python string.
        """
        return obj.get_absolute_url()
    
    def description(self, obj):
        """
        Takes the object returned by get_object() and returns the feed's
        description as a normal Python string.
        """
        return "Recent Articles by %s on Flove" % obj
    
    def items(self, obj):
        """
        Takes the object returned by get_object() and returns a list of
        seven recent items to publish in this feed.
        """
        return Article.objects.filter(writer=obj).filter(article_status='p')[:7]
    
    def item_title(self, item):
        """
        Return the title of the article.
        """
        return item.title

    def item_description(self, item):
        """
        Return the text of the article.
        """
        return item.text