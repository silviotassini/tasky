from django import forms
from tasks.models import Task, SubTask
from django.utils import timezone

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'value': timezone.now().strftime('%Y-%m-%d')}),
            'estimated_end_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = '__all__'
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'estimated_end_date': forms.DateInput(attrs={'type': 'date'}),
            'actual_end_date': forms.DateInput(attrs={'type': 'date'}),
        }
