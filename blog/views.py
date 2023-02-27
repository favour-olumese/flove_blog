from django.shortcuts import render, redirect, get_object_or_404
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.generic import ListView, DetailView
from blog.models import Article, Writer
from django.contrib.auth.mixins import LoginRequiredMixin,  UserPassesTestMixin
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.utils.text import slugify
from uuid import uuid4


def home(request):
    """Blog home page."""

    hello = 'Welcome to Flove blog. Nice to have you here.'

    context = {
        'hello': hello
    }

    return render(request, 'blog/index.html', context)


def register_user(request):
    """View for user registration."""

    form = UserRegistrationForm()

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            form.save(commit=False)
            user_email = form.cleaned_data['email']
            user_username = form.cleaned_data['username']
            user_password = form.cleaned_data['password1']

            user = User.objects.create_user(username=user_username, email=user_email, password=user_password)
            
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


class ArticleListView(ListView):
    """List view of all public articles."""

    queryset = Article.objects.filter(article_status='p')


class ArticleDetailView(DetailView):
    """Content of each article view."""

    model = Article
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def get_object(self, queryset=None):
        """Function to assign field of the User model that would be used for the url kwarg."""

        article_url = self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)


class ArticleCreateView(LoginRequiredMixin, CreateView):
    """View for creating new articles."""

    model = Article
    fields = ['article_img', 'title', 'text', 'article_status']

    def form_valid(self, form):
        """Assigns article to current user and use article title to create url path."""

        article_writer = Writer.objects.filter(user=self.request.user)[0]
        form.instance.writer = article_writer

        # Adding random hash the end of article title to make url unique.
        random_slug = str(uuid4())[:8]
        form.instance.article_url = slugify(form.instance.title + ' ' + random_slug)

        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating articles."""

    model = Article
    fields = ['article_img', 'title', 'text', 'article_status']
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def test_func(self):
        """"Works with UserPassesTestMixin.

        Returns True when current user is the article onwer;
        but returns False when current user is not the article onwer.
        """

        article = Article.objects.filter(article_url=self.kwargs['article_url'])[0]
        return article.writer.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not article owner to the article page.

        By default, test_func redirects user who do not own the article to the 403 page.
        """
        
        return redirect(reverse_lazy('article-detail', kwargs={'article_url':str(self.kwargs['article_url']), 'username':str(self.kwargs['username'])}))

    def get_object(self, queryset=None):
        """Function to assign article_url of the Article model to the url kwarg."""

        article_url = self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    """View for deleting articles."""

    model = Article
    success_url = reverse_lazy('articles')
    slug_url_kwarg = 'article_url'
    slug_url_kwarg2 = 'username'

    def  get_object(self, queryset=None):
        """Function to assign article_url of the Article model to the url kwarg."""

        article_url =self.kwargs.get(self.slug_url_kwarg)
        user_name = self.kwargs.get(self.slug_url_kwarg2)

        return get_object_or_404(self.model, article_url=article_url)


class MyArticleListView(LoginRequiredMixin, ListView):
    """"List of all public and unlisted articles.
    
    Each writer can only access his or her own list.
    """

    template_name = 'blog/writer_articles.html'
    context_object_name = 'my_articles'

    def get_queryset(self):
        """Returns public and unlisted article of logged in writer."""

        return Article.objects.filter(writer=self.request.user.writer).exclude(article_status='d')


class ArticleDraftListView(LoginRequiredMixin, ListView):
    """View for drafts."""

    template_name = 'blog/writer_draft.html'

    def get_queryset(self):
        """
        Gets articles of writer that have the draft status.
        """
        user = self.request.user.writer

        return Article.objects.filter(writer=user, article_status='d')


@login_required
def article_filter(request):
    """Function for writer to view all published, unlisted, or public articles."""

    article_status = request.GET.get('article_status')
    writer = request.user.writer

    # All articles
    if (article_status == 'a'):
        return HttpResponseRedirect(reverse('my-articles'))

    articles = Article.objects.filter(writer=writer, article_status=article_status)

    context = {
        'my_articles': articles,
        'article_status': article_status,
        'writer': writer,
    }

    return render(request, 'blog/writer_articles.html', context)


class WriterCreateView(LoginRequiredMixin, CreateView):
    """View for creating writer profile."""

    model = Writer
    fields = ['profile_picture', 'first_name', 'last_name', 'bio', 'website_url', 'linkedin_url', 'display_email']
    success_url = ''

    def form_valid(self, form):
        """Assigns writer's detail to current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)


class WriterUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """View for updating user details."""
    
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

        Returns True when current user is the profile onwer;
        but returns False when current user is not.
        """

        username = self.kwargs['username']
        user_id = User.objects.filter(username=username).values()[0]['id']
        writer = Writer.objects.filter(user=user_id)[0]

        return writer.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not profile owner to the user page.

        By default, test_func redirects user who do not own the profile to the 403 page.
        """
        
        return redirect(reverse_lazy('writer', kwargs={'username':self.kwargs['username']}))


class WriterDetailView(DetailView):
    """View of writer page."""

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
