from django.contrib import admin
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe
from .models import Task, Event


class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ("created",)


# Register your models here.
myModels = [Task, Event]
admin.site.register(myModels)
