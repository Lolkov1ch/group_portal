from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Post, Topic, Attachment, Tag

class PostForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        widget=forms.FileInput(),
        label=_('Вкладення'),
        help_text=_('Дозволені формати: png, jpg, jpeg, gif, pdf, zip, rar, 7z, txt, mp4')
    )

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
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['attachments'].widget.attrs['multiple'] = True

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