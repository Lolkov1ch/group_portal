from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Topic, Attachment

class PostForm(forms.ModelForm):
    # Видаляємо поле attachments з форми зовсім
    # Файли будемо обробляти напряму через request.FILES
    
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
    class Meta:
        model = Topic
        fields = ["title"]
        widgets = {
            "title": forms.TextInput(attrs={
                "placeholder": "Назва теми"
            })
        }

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file']