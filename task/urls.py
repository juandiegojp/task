"""djangocrud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, include
from task import views

urlpatterns = [    
    path('', views.home, name="home"),
    path('tasks/', views.tasks, name="tasks"),
    path('tasks/completed/', views.tasks_completed, name="task_completed"),
    path('tasks/<int:task_id>/pdf', views.g_PDF, name="generatePDF"),
    path('task/create', views.create_task, name="create_task"),
    path('task/<int:task_id>/', views.task_detail, name="task_detail"),
    path('task/<int:task_id>/complete', views.task_complete, name="task_complete"),
    path('task/<int:task_id>/delete', views.task_delete, name="task_delete"),
    path('signup/', views.signup, name="signup"),
    path('signin/', views.signin, name="signin"),
    path('logout/', views.signout, name="logout"),
]