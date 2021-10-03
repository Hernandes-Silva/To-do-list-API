from django import forms
from django.forms import widgets
from tasks.models import Task
class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        exclude = ('slug','user')
    def __init__(self, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs = {'class': 'form-control'}