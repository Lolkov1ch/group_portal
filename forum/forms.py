from django import forms
from .models import Post, Topic

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "cols": 60, "placeholder": "Ваша відповідь..."})
        }

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["title"]