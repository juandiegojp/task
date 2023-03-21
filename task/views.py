from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect
from django.db import IntegrityError

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    else:
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 == password2:
            try:
                username = request.POST['username']
                user = User.objects.create_user(
                    username=username, password=password1)
                user.save()
                login(request, user)
                return redirect('task')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Passwords do not match'
                })

def signout(request):
    logout(request)
    return redirect('home')

def task(request):
    return render(request, 'task.html')