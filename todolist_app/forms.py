from django import forms
from todolist_app.models import TaskList
from django.http import HttpResponse

class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['task', 'done']