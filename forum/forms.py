from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Topic, Attachment, Tag

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={
                "rows": 4, 
                "cols": 60, 
                "placeholder": "Ваша відповідь..."
            })
        }

class TopicForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Теги"
    )
    
    class Meta:
        model = Topic
        fields = ["title", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Назва теми"
            })
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']