from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

# Models
from blog.models import Article, Writer, Comment, Reply

# Make login a requirement
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required

# For user to create account and email verification to be done.
from .forms import UserRegistrationForm
from django_email_verification import send_email

# For creation of article's url
from django.utils.text import slugify
from uuid import uuid4

# For handling of text to speech for article audio.
import pyttsx3
import os

# Using rich text audio to contain hmtl tags.
# This filters our the tags and unicode characters
from django.utils.html import strip_tags    # Removes html tags
from html import unescape   # Converts unicode to Python equivalent
from unicodedata import normalize # Convert Python unicode character to text equivalent


# For calculating how long it would take to read an article
import time

# Forms for comment and reply
from blog.forms import CommentForm, ReplyForm

# For displaying error message for comments and replies
from django.contrib import messages

# For making search form
from django.db.models import Q


def home(request):
    """Blog home page."""

    hello = 'Welcome to Flove blog. Nice to have you here.'

    context = {
        'hello': hello
    }

    return render(request, 'blog/index.html', context)


def register_user(request):
    """Registers new users."""

    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']

            user = User.objects.create_user(
                username=user_username, 
                email=user_email, 
                password=user_password,
                )

            # Make user unactive until they click link to token in email
            user.is_active = False

            send_email(user)

            # # Check if email already exist in the database.
            # email_exist = User.objects.get(email=user_email)

            # if email_exist:
            #     context = {
            #         'form':form,
            #         'email_error':'Email already exist.'
            #     }
            #     return render(request, 'registration/register.html', context)
            

            return HttpResponseRedirect(reverse('login'))

    return render(request, 'registration/register.html', {'form':form})


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes user account."""
    model = User
    slug_url_kwarg = 'username'
    template_name = 'blog/user_confirm_delete.html'
    success_url = reverse_lazy('home')

    def  get_object(self, queryset=None):
        """Assigns username of the User model to the url kwarg."""

        user = self.kwargs.get(self.slug_url_kwarg)

        return get_object_or_404(self.model, username=user)
    
    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user owner of account
        but returns False when current user is not.
        """

        username = User.objects.filter(username=self.kwargs['username'])[0]
        return username == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not user of the account to the home page.

        By default, test_func redirects user who do not own the account to the 403 page.
        """
        
        return redirect(reverse_lazy('home'))


class ArticleListView(ListView):
    """Lists all public articles."""

    # model = Article
    template_name = 'blog/article_list.html'
    queryset = Article.objects.filter(article_status='p')
    paginate_by = 10

    def get_queryset(self, **kwargs):
        """Handles query set for both all articles and viewing saved articles.
        
        - If request is for all articles, it displays all public articles,
        else, if it is for saved articles, articles saved by 
        requesting user are displayed
        - To access saved articles, user must be logged in. This is handled
        in the urls.py file
        """
        queryset = super().get_queryset()

        current_url = self.request.path
        if current_url == reverse('articles'):
            queryset = queryset

        # Queryset for saved articles
        elif current_url == reverse('saved-articles'):

            # Check if users has created their writer profile.
            if hasattr(self.request.user, 'writer'):
                queryset = Writer.objects.get(id=self.request.user.writer.id).saved_articles.all()
            else:
                return

        return queryset


class ArticleDetailView(DetailView):
    """Display content of articles"""

    model = Article
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def get_object(self, queryset=None):
        """Function to assign field of the User model that would be used for the url kwarg."""

        article_url = self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)

    def get_context_data(self, **kwargs):
        """Function to:
        - Add article reading time to template.
        - Add other article of the writer for reader to read.
        """
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get article text and title
        article_url = self.kwargs['article_url']
        article_text = Article.objects.filter(article_url=article_url).values()[0]['text']
        article_title = Article.objects.filter(article_url=article_url).values()[0]['title']

        # Article reading time
        word_num = len(article_text.split() + article_title.split()) 
        word_secs = (word_num / 200) * 60  # 200 words per minutes

        if word_secs < 60:
            article_time  = 'Less than a minute'
        else:
            article_time = time.strftime('%M mins %S secs', time.gmtime(word_secs))

        context['article_time'] = article_time

        # More articles by same writer for readers to read
        writer_username = self.kwargs['username']
        user_id = User.objects.filter(username=writer_username).values()[0]['id']
        writer  = Writer.objects.get(user=user_id)

        more_article = Article.objects.filter(writer=writer).exclude(article_url=article_url).exclude(article_status='d')[:3]
        context['more_article'] = more_article

        return context


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """Creates new articles."""

    model = Article
    fields = ['article_img', 'title', 'text', 'article_status', 'display_audio']

    def form_valid(self, form):
        """
        - Assigns article to current user
        - Use article's title and uuid to create url path of article.
        - Create article audio using pyttsx3 module
        """

        # Assigns the writer field to the current user.
        user_name = self.request.user
        form.instance.writer = user_name.writer

        # Adding random hash the end of article title to make url unique.
        random_slug = str(uuid4())[:8]
        article_url_path = form.instance.title + ' ' + random_slug
        form.instance.article_url = slugify(article_url_path)

        # Saving article audio
        text_with_tags_and_unicode = form.instance.text
        text_with_only_unicode = strip_tags(text_with_tags_and_unicode)  # Remove tags
        text_with_python_unicode = unescape(text_with_only_unicode)  # Convert unicode to python equivalent
        cleaned_text = normalize("NFKC", text_with_python_unicode)  # Convert to normal text

        title_and_text = form.instance.title + '\n' + cleaned_text
        audio_name = str(user_name) + '_' + form.instance.article_url + '.mp3'

        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(title_and_text, 'temp_audio.mp3')
        engine.runAndWait()

        form.instance.article_audio.save(audio_name, open('temp_audio.mp3', 'rb'))

        # Delete temporary audio after saving file to audio FileField
        os.remove('temp_audio.mp3')

        return super().form_valid(form)
    
    def get(self, request, *args, **kwargs):
        """Redirects users who have created their writer profile already 
        to the writer's update page.
        
        If user has not created a profile, they are taken to the profile
        creation page.
        """
        username = request.user

        if Writer.objects.filter(user=username).exists():
            return super().get(request, *args, *kwargs)
        
        messages.info(request, 'You have to fill in your writer profile before you can create an article.')
        return redirect('new-writer')


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Updates already created articles."""

    model = Article
    fields = ['article_img', 'title', 'text', 'article_status', 'display_audio']
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user is the article owner;
        but returns False when current user is not the article owner.
        """

        article = Article.objects.filter(article_url=self.kwargs['article_url'])[0]
        return article.writer.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not article owner to the article page.

        By default, test_func redirects user who do not own the article to the 403 page.
        """
        
        return redirect(reverse_lazy(
                        'article-detail',
                        kwargs={'article_url':str(self.kwargs['article_url']),
                                'username':str(self.kwargs['username'])}))
    
    def form_valid(self, form):
        """Update article audio file."""
        
        # Delete former audio of updated article
        if form.instance.article_audio:
            form.instance.article_audio.delete()

        username = str(self.request.user)
        article_url = self.kwargs['article_url']

        # Title and text to be converted to speech.
        text_with_tags_and_unicode = form.instance.text
        text_with_only_unicode = strip_tags(text_with_tags_and_unicode)  # Remove tags
        text_with_python_unicode = unescape(text_with_only_unicode)  # Convert unicode to python equivalent
        cleaned_text = normalize("NFKC", text_with_python_unicode)  # Convert to normal text

        title_and_text = form.instance.title + '\n' + cleaned_text
        audio_name = username + '_' + article_url + '.mp3'

        # Text to speech
        engine = pyttsx3.init()
        engine.setProperty('rate', 150)
        engine.save_to_file(title_and_text, 'temp_audio.mp3')
        engine.runAndWait()

        # Save audio file to article.article_audio field
        form.instance.article_audio.save(audio_name, open('temp_audio.mp3', 'rb'))

        # Remove unneeded file created by engine.save_to_file
        os.remove('temp_audio.mp3')

        return super().form_valid(form)

    def get_object(self, queryset=None):
        """Function to assign article_url of the Article model to the url kwarg."""

        article_url = self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)


class ArticleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes existing articles."""

    model = Article
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def  get_object(self, queryset=None):
        """Assigns article_url of the Article model to the url kwarg."""

        article_url =self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)
    
    def get_success_url(self):
        """Redirects users to their page after they delete an article."""
        return reverse_lazy('writer', args=(self.request.user,))

    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user is the article owner;
        but returns False when current user is not the article owner.
        """

        article = Article.objects.filter(article_url=self.kwargs['article_url'])[0]
        return article.writer.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not article owner to the article page.

        By default, test_func redirects user who do not own the article to the 403 page.
        """
        
        return redirect(reverse_lazy(
                        'article-detail',
                        kwargs={'article_url':str(self.kwargs['article_url']),
                                'username':str(self.kwargs['username'])}))


@login_required
def article_filter(request):
    """Filters published, unlisted, or public articles for requesting writer."""

    article_status = request.GET.get('article_status')
    writer = request.user.writer

    # All articles
    if (article_status == 'a'):
        return HttpResponseRedirect(reverse('writer', args=(request.user,)))

    articles = Article.objects.filter(writer=writer, article_status=article_status)

    context = {
        'article_list': articles,
        'article_status': article_status,
        'writer': writer,
    }

    return render(request, 'blog/writer_detail.html', context)


@login_required
def article_likes(request, username, article_url):
    """Function for liking articles
    
    - Writers who likes an article are added to the 
    likes field of the Article model.
    - If GET method is used, the users are redirected the article.
    - If POST method is used the data is saved in the database and 
    a JSON response is sent to update the page asynchronously
    - Users yet to create their writer profile are redirected 
    to the writer creation template.
    - Users not logged in are redirected to the login  page.

    username        the user requesting to like the article
    article_url     the url of the article being liked
    """

    path_url = request.path

    path_url_list = path_url.split('/')

    # Turncate the '/like' portion of the url.
    article_path = '/'.join(path_url_list[:-1])

    if request.method == 'POST':
        # Check if user already have a writer profile
        if hasattr(request.user, 'writer'):
            article = get_object_or_404(Article, id=request.POST.get('article_id'))

            if article.likes.filter(id=request.user.writer.id).exists():
                article.likes.remove(request.user.writer)
                button_value = '[\uf087'
                title_value = 'Like'
            else:
                article.likes.add(request.user.writer)
                button_value = '[\uf164'
                title_value = 'Unlike'
            
            article_likes = article.likes.count()
            status = 200

            context = {
                'article_likes': article_likes,
                'status': status,
                'button_value': button_value,
                'title_value': title_value,
            }

        # Redirects users yet to create a writer profile to create one.
        else:
            messages.info(request, 'You have to fill in your writer profile before you can like an article.')
            writer_profile_page = HttpResponseRedirect(reverse_lazy('new-writer')).url
            status = 302

            context = {
                'writer_profile_page': writer_profile_page,
                'status': status,
            }

        return JsonResponse(context)

    return HttpResponseRedirect(article_path)


@login_required
def save_article(request, username, article_url):
    """Function for saving/bookmarking of articles by writers.
    
    - Articles saved by a writer are added to the saved_articles 
    field of the Writer.
    - Users yet to create their writer profile are redirected 
    to the writer creation template.
    - Users not logged in are redirected to the login page.

    username        the user requesting to save the article
    article_url     the url of the article being saved
    """

    path_url = request.path

    path_url_list = path_url.split('/')

    # Turncate the '/save' portion of the url.
    article_path = '/'.join(path_url_list[:-1])

    if request.method == 'POST':
        article_id = request.POST.get('article_id')

        # Check if user already have a writer profile
        if hasattr(request.user, 'writer'):
            writer = request.user.writer

            if writer.saved_articles.filter(id=article_id).exists():
                writer.saved_articles.remove(article_id)
                button_value = '\uf097'
                title_value = 'Save'
            else:
                writer.saved_articles.add(article_id)
                button_value = '\uf02e'
                title_value = 'Unsave'

            status = 200

            context = {
                'button_value': button_value,
                'status': status,
                'title_value': title_value,
            }

        # Redirects users yet to create a writer profile to create one.
        else:
            messages.info(request, 'You have to fill in your writer profile before you can save an article.')
            writer_profile_page = HttpResponseRedirect(reverse_lazy('new-writer')).url
            status = 302

            context = {
                'writer_profile_page': writer_profile_page,
                'status': status,
            }

        return JsonResponse(context)

    return HttpResponseRedirect(article_path)


class WriterCreateView(LoginRequiredMixin, CreateView):
    """Creates writer profile."""

    model = Writer
    fields = ['profile_picture', 'first_name', 'last_name', 'bio', 'website_url', 'linkedin_url', 'display_email']
    success_url = ''  # TODO: Change the success_url

    def form_valid(self, form):
        """Assigns writer's detail to current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get(self, request, *args, **kwargs):
        """Redirects users who have created their writer profile already 
        to the writer's update page.
        
        If user has not created a profile, they are taken to the profile
        creation page.
        """
        username = request.user

        if Writer.objects.filter(user=username).exists():
            return redirect(reverse_lazy('writer-profile-update', kwargs={'username':username}))

        return super().get(request, *args, *kwargs)


class WriterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Updates writer's profile."""
    
    model = Writer
    fields = ['profile_picture', 'first_name', 'last_name', 'bio', 'website_url', 'linkedin_url', 'display_email']
    slug_url_kwarg = 'username'

    def get_object(self, queryset=None):
        """Function to assign field of the User model that would be used for the url kwarg."""
        
        # Get writer user_id
        username = self.kwargs.get(self.slug_url_kwarg)
        user_id = User.objects.filter(username=username).values()[0]['id']
        
        return get_object_or_404(self.model, user=user_id)

    def test_func(self):
        """"Works with UserPassesTestMixin.

        - Returns True when current user is the profile owner;
        but returns False when current user is not.
        - It also returns False the current user tries to access
        their profile before creating it.
        """

        username = self.kwargs['username']
        user_id = User.objects.filter(username=username).values()[0]['id']
        if Writer.objects.filter(user=user_id).exists():
            writer = Writer.objects.filter(user=user_id)[0]

            return writer.user == self.request.user
        else:
            return False

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not profile owner to the user page.

        - By default, test_func redirects user who do not own 
        the profile to the 403 page.
        - If current user tries to update their profile before creating it, 
        they are redirected to the profile crreation page.
        """
        username = self.kwargs.get(self.slug_url_kwarg)
        user_id = User.objects.filter(username=username).values()[0]['id']
        
        if Writer.objects.filter(user=user_id).exists():
            return redirect(reverse_lazy('writer', kwargs={'username':self.kwargs['username']}))
        else:
            return HttpResponseRedirect(reverse_lazy('new-writer'))


class WriterDetailView(DetailView):
    """Displays writer's details and articles written."""

    model = Writer
    slug_url_kwarg = 'username'
    template_name = 'blog/writer_detail.html'

    def get_context_data(self, **kwargs):
        """Function to add article of user as context in the template."""
        
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # Get the username in the url
        user_name = self.kwargs['username']
        user = User.objects.filter(username=user_name)[0]
        
        context['article_list'] = Article.objects.filter(writer=user.writer).exclude(article_status='d')
        return context

    def get_object(self, queryset=None):
        """Function to assign field of the User model that would be used for the url kwarg."""

        # Get writer user_id
        username = self.kwargs.get(self.slug_url_kwarg)
        user_id = User.objects.filter(username=username).values()[0]['id']

        return get_object_or_404(self.model, user=user_id)


@login_required()
def comment(request, username, article_url):
    """Function for commenting on articles.
    
    - Users yet to create their writer profile are redirected 
    to the writer creation template.
    - Users not logged in are redirected to the login page.

    username        the user requesting to save the article
    article_url     the url of the article being saved
    """

    if request.method == 'POST':
        
        # Check if user already have a writer profile
        if hasattr(request.user, 'writer'):
            form = CommentForm(request.POST)

            if form.is_valid():
                form.save(commit=False)
                comment_text = form.cleaned_data['text']
                article_id = request.POST['article_id']
                article = Article.objects.filter(id=article_id)[0]

                commenter = request.user.writer
                
                Comment.objects.create(
                    text=comment_text,
                    commenter=commenter,
                    article=article,
                )

            # Using the message field to display errors
            else:
                messages.error(request, 'Text field required.')

        # Redirects users yet to create a writer profile to create one.
        else:
            messages.info(request, 'You have to fill in your writer profile '
                          'before you can comment on an article.')

            return HttpResponseRedirect(reverse_lazy('new-writer'))

    return HttpResponseRedirect(reverse('article-detail', args=(username, article_url)))


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes user's comment."""

    model = Comment

    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user is the comment owner;
        but returns False when current user is not the comment owner.
        """

        article = Article.objects.filter(article_url=self.kwargs['article_url'])[0]
        comment = Comment.objects.filter(article=article).get(id=self.kwargs['pk'])
        return comment.commenter.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not article owner to the article page.

        By default, test_func redirects user who do not own the comment to the 403 page.
        """
        
        return redirect(reverse_lazy(
                        'article-detail',
                        kwargs={'article_url':str(self.kwargs['article_url']),
                                'username':str(self.kwargs['username'])}))

    def get_success_url(self):
        """Redirects users to their article page after they delete their comment."""
        return reverse_lazy('article-detail',
                            kwargs={'article_url':self.kwargs['article_url'],
                                    'username':self.kwargs['username']})


@login_required()
def reply(request, username, article_url):
    """Function for replying to comments.
    
    - Users yet to create their writer profile are redirected 
    to the writer creation template.
    - Users not logged in are redirected to the login page.

    username        the user requesting to save the article
    article_url     the url of the article being saved
    """

    if request.method == 'POST':
        # Check if user already have a writer profile
        if hasattr(request.user, 'writer'):            
            form = ReplyForm(request.POST) # binding the reply text to the form

            if form.is_valid():
                form.save(commit=False)
                reply_text = form.cleaned_data['reply_text']

                # Related Article
                article_id = request.POST['article_id']
                article = Article.objects.filter(id=article_id)[0]

                # Related Comment
                comment_id = request.POST['comment_id']
                comment_query = Comment.objects.filter(id=comment_id)[0]

                # Replier
                replier = request.user.writer

                Reply.objects.create(
                    reply_text=reply_text,
                    replier=replier,
                    article=article,
                    comment=comment_query,
                )

            # Using the message field to display errors
            else:
                messages.error(request, 'Text field required.')
        
        # Redirects users yet to create a writer profile to create one.
        else:
            messages.info(request, 'You have to fill in your writer profile '
                          'before you can reply a comment.')

            return HttpResponseRedirect(reverse_lazy('new-writer'))

    return HttpResponseRedirect(reverse('article-detail', args=(username, article_url)))


class ReplyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Deletes a user's reply."""

    model = Reply

    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user is the reply owner;
        but returns False when current user is not the reply owner.
        """

        article = Article.objects.filter(article_url=self.kwargs['article_url'])[0]
        reply = Reply.objects.filter(article=article).get(id=self.kwargs['pk'])
        return reply.replier.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not reply owner to the article page.

        By default, test_func redirects user who do not own the reply to the 403 page.
        """
        
        return redirect(reverse_lazy(
                        'article-detail',
                        kwargs={'article_url':str(self.kwargs['article_url']),
                                'username':str(self.kwargs['username'])}))

    def get_success_url(self):
        """Redirects users to their article page after they delete their comment."""
        return reverse_lazy('article-detail',
                            kwargs={'article_url':self.kwargs['article_url'],
                                    'username':self.kwargs['username']})


def search(request):
    search_data = request.GET.get('search')

    writer_list = Writer.objects.filter(Q(first_name__icontains=search_data) |
                                        Q(last_name__icontains=search_data) |
                                        Q(user__email=search_data) |
                                        Q(user__username=search_data)
                                        )

    article_list = Article.objects.filter(Q(title__icontains=search_data) |
                                          Q(text__icontains=search_data) |
                                          Q(writer__first_name__icontains=search_data) |
                                          Q(writer__last_name__icontains=search_data) |
                                          Q(writer__user__email=search_data) |
                                          Q(writer__user__username=search_data)
                                          )

    query_count = len(writer_list) + len(article_list)

    context = {
        'search_data': search_data,
        'writer_list' : writer_list,
        'article_list' : article_list,
        'query_count' : query_count,
    }

    return render(request, 'blog/article_list.html', context)


@login_required
def writer_settings_page(request):
    user = request.user

    context = {
        'user': user,
    }
    return render(request, 'blog/writer_settings.html', context)