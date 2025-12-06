from django import forms
from .models import MediaItem

ALLOWED_MIME_TYPES = {
    'image/png': 'PNG',
    'image/jpeg': 'JPEG',
    'image/jpg': 'JPG',
    'image/gif': 'GIF',
    'video/mp4': 'MP4',
    'video/quicktime': 'MOV',
    'video/x-msvideo': 'AVI',
    'video/x-matroska': 'MKV',
    'video/webm': 'WEBM'
}


class MediaItemForm(forms.ModelForm):
    class Meta:
        model = MediaItem
        fields = ['title', 'description', 'file', 'media_type', 'game_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва медіафайлу',
                'maxlength': '200'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Опис (необов\'язково)'
            }),
            'file': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*,video/*'
            }),
            'media_type': forms.Select(attrs={
                'class': 'form-select'
            }),
            'game_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Назва гри (необов\'язково)',
                'maxlength': '100'
            }),
        }
        labels = {
            'title': 'Назва',
            'description': 'Опис',
            'file': 'Файл',
            'media_type': 'Тип медіа',
            'game_name': 'Назва гри',
        }
        help_texts = {
            'file': 'Максимальний розмір: 20 МБ. Формати: PNG, JPG, GIF, MP4, MOV, AVI, MKV, WEBM',
            'media_type': 'Оберіть тип медіафайлу',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if title:
            title = title.strip()
            if len(title) < 3:
                raise forms.ValidationError(
                    "Назва повинна містити щонайменше 3 символи."
                )
        return title

    def clean_file(self):
        file = self.cleaned_data.get('file')
        
        if not file:
            raise forms.ValidationError("Файл обов'язковий.")

        filename = file.name
        ext = filename.split('.')[-1].lower()
        
        allowed_extensions = MediaItem.ALLOWED_EXTENSIONS
        
        if ext not in allowed_extensions:
            raise forms.ValidationError(
                f"Розширення '.{ext}' не дозволене. "
                f"Дозволені розширення: {', '.join(allowed_extensions)}"
            )
        
        max_size = 20 * 1024 * 1024  
        if file.size > max_size:
            raise forms.ValidationError(
                f"Розмір файлу не може перевищувати 20 МБ. "
                f"Розмір вашого файлу: {file.size / (1024 * 1024):.2f} МБ"
            )
        
        min_size = 1024  
        if file.size < min_size:
            raise forms.ValidationError(
                "Файл занадто малий. Мінімальний розмір: 1 КБ"
            )
        
        if hasattr(file, 'content_type'):
            if file.content_type not in ALLOWED_MIME_TYPES:
                raise forms.ValidationError(
                    f"Тип файлу '{file.content_type}' не дозволений. "
                    f"Дозволені типи: {', '.join(ALLOWED_MIME_TYPES.values())}"
                )
        
        return file
    
    def clean(self):
        cleaned_data = super().clean()
        
        file = cleaned_data.get('file')
        media_type = cleaned_data.get('media_type')
        
        if file and media_type == 'unknown':
            ext = file.name.split('.')[-1].lower()
            if ext in MediaItem.IMAGE_EXTENSIONS:
                if 'screenshot' not in file.name.lower():
                    cleaned_data['media_type'] = 'photo'
                else:
                    cleaned_data['media_type'] = 'screenshot'
            elif ext in ['mp4', 'mov', 'avi', 'mkv', 'webm']:
                cleaned_data['media_type'] = 'video'
        
        return cleaned_data