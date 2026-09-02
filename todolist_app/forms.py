from django import forms
from todolist_app.models import TaskList


class TaskForm(forms.ModelForm):
    class Meta:
        model = TaskList
        fields = ['title', 'task', 'done']
        widgets = {
            'title': forms.HiddenInput(),
            'done': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False

    def clean(self):
        cleaned_data = super().clean()
        task = cleaned_data.get('task')
        if task and not cleaned_data.get('title'):
            cleaned_data['title'] = task[:200]
        return cleaned_data
