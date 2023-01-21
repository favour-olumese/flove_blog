from django.shortcuts import render
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from verify_email.email_handler import send_verification_email


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
            # user_email = form.cleaned_data['email']

            # # Check if email already exist in the database.
            # email_exist = User.objects.get(email=user_email)

            # if email_exist:
            #     context = {
            #         'form':form,
            #         'email_error':'Email already exist.'
            #     }
            #     return render(request, 'registration/register.html', context)
            
            inactive_user = send_verification_email(request, form)
            # form.save()
            # From Django-Verify-Email 2.0.3 docs
            # The user is already being saved as inactive and you don't have to .save() it explicitly.
            

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'registration/register.html', {'form':form})