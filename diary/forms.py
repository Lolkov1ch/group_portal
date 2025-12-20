from django import forms
from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['student', 'subject', 'score', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
        }