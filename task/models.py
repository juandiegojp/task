from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True, blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.title} - {self.user.username}'

class Events(models.Model):
    title = models.CharField(max_length=100)
    endtime = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    
    def __str__(self):
        return f'{self.title}'
    