from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render

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
                return HttpResponse('User created successfully')
            except:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'Username already exists'
                })
        else:
            return HttpResponse('Passwords do not match')


def home(request):
    return render(request, 'home.html')
