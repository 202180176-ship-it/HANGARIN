from django import forms
from .models import Task, Note

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'status', 'category', 'priority']
        widgets = {
            'deadline': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        # Based on your ERD, a Note needs a Task and Content [cite: 16, 20]
        fields = ['task', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Enter your note here...', 'rows': 3}),
        }
        
