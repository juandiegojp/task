import json
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm #Formularios
from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator #Paginacion
#Calendario
from datetime import datetime
from django.views import generic
from django.utils.safestring import mark_safe

from .models import * #Importa todos los modelos
from .forms import TaskForm #forms.py

def home(request):
    all_events = Event.objects.all()

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:  
        event_arr = []
        all_events = Event.objects.all()
        
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.title
            start_date = datetime.strptime(str(i.start_time.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            end_date = datetime.strptime(str(i.end_time.date()), "%Y-%m-%d").strftime("%Y-%m-%d")
            event_sub_arr['start'] = start_date
            event_sub_arr['end'] = end_date
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr), content_type="application/json")
    return render(request,'home.html', {"events":all_events,})


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
                return redirect('tasks')
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


def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,
                            username=request.POST['username'],
                            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm,
                'error': 'Username or password is incorrect'
            })
        else:
            login(request, user)
            return redirect('home')


@login_required
def tasks(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=True).order_by('-important')
    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'task.html', {
        'tasks': page_obj
    })


@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(
        user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    paginator = Paginator(tasks, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'task.html', {
        'tasks': page_obj
    })


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form': TaskForm
        })
    else:
        try:
            new_task = TaskForm(request.POST).save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Provide valide data'
            })


@login_required
def task_detail(request, task_id):
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {
            'task': task,
            'form': form
        })
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {
                'task': task,
                'form': form,
                'error': "Error updating task"
            })


@login_required
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')


@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')

def event(request):
    all_events = Task.objects.all()

    # if filters applied then get parameter and filter based on condition else return object
    if request.GET:  
        event_arr = []
        all_events = Task.objects.all()
        
        for i in all_events:
            event_sub_arr = {}
            event_sub_arr['title'] = i.title
            event_arr.append(event_sub_arr)
        return HttpResponse(json.dumps(event_arr), content_type="application/json")
    return render(request,'home.html', {"events":all_events,})