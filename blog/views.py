from django.shortcuts import render
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django_email_verification import send_email



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

            user = get_user_model().objects.create(username=user_username, email=user_email, password=user_password)
            user.is_active = False  # Example
            send_email(user)

            # # Check if email already exist in the database.
            # email_exist = User.objects.get(email=user_email)

            # if email_exist:
            #     context = {
            #         'form':form,
            #         'email_error':'Email already exist.'
            #     }
            #     return render(request, 'registration/register.html', context)
            

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'registration/register.html', {'form':form})