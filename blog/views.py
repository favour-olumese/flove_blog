from django.shortcuts import render, redirect
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



def home(request):
    hello = 'Welcome to Flove blog. Nice to have you here.'

    context = {
        'hello': hello
    }

    return render(request, 'blog/index.html', context)


def register_user(request):
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
    model = Article

class MyArticleListView(ListView):
    # queryset = Article.objects.filter(user=self.request.user)
    template_name = 'blog/writer_articles.html'
    context_object_name = 'my_articles'

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['article_img', 'title', 'text']
    success_url = '/articles/'

    def form_valid(self, form):
        """Method to assign article to current user."""
        article_writer = Writer.objects.filter(user=self.request.user)[0]
        form.instance.writer = article_writer
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    queryset = Article.objects.all()
    fields = ['article_img', 'title', 'text']

    def test_func(self):
        """"Works with UserPassesTestMixin.
        Returns True when current user is the artticle onwer;
        but returns False when current user is not the article onwer.
        """

        article = Article.objects.filter(id=self.kwargs['pk'])[0]
        return article.writer.user == self.request.user

    def handle_no_permission(self, *kwargs):
        """Redirect current user who is not article owner to the article page.
        By default, test_func redirects user who do not own the article to the 403 page.
        """
        
        return redirect(reverse_lazy('article-detail', kwargs={'pk': self.kwargs['pk']}))

class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    model = Article
    success_url = reverse_lazy('articles')


class WriterCreateView(LoginRequiredMixin, CreateView):
    model = Writer
    fields = ['profile_picture', 'first_name', 'last_name', 'bio']
    success_url = ''

    def form_valid(self, form):
        """Method to assign writer's detail to current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)
