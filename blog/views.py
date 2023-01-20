from django.shortcuts import render
from .forms import UserRegistrationForm
from django.http import HttpResponseRedirect
from django.urls import reverse

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
            form.save() 

            return HttpResponseRedirect(reverse('home'))

    return render(request, 'registration/register.html', {'form':form})