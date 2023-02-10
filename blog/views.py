from django.shortcuts import render
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from django.views.generic import ListView, DetailView
from blog.models import Article, Writer
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView



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


class ArticleDetailView(DetailView):
    model = Article


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['article_img', 'title', 'text']
    success_url = '/articles/'

    def form_valid(self, form):
        """Method to assign article to current user."""
        written_by = Writer.objects.filter(user=self.request.user)[0]
        form.instance.writer = written_by
        return super().form_valid(form)


class WriterCreateView(LoginRequiredMixin, CreateView):
    model = Writer
    fields = ['profile_picture', 'first_name', 'last_name', 'bio']
    success_url = ''

    def form_valid(self, form):
        """Method to assign writer's detail to current user."""
        form.instance.user = self.request.user
        return super().form_valid(form)
