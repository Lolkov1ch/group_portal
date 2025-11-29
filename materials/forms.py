from django import forms
from .models import Material
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

import os

class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "title", "description", "category", "engine", "file_type", "file_link", "file_upload", "is_published"
        ]
    
    # Перевірка форми
    def clean(self):
        cleaned_data = super().clean() # Очищення даних

        file_type = cleaned_data.get('file_type')
        file_link = cleaned_data.get('file_link')
        file_upload = cleaned_data.get('file_upload')

        if not file_type:
            return cleaned_data

        # Перевірка посилань і відео
        if file_type in [Material.FileTypeChoices.LINK, Material.FileTypeChoices.VIDEO]:
            if not file_link:
                self.add_error("file_link", "Це поле обов'язкове для типу 'Посилання' або 'Відео'.")
            
            else:
                url_validator = URLValidator()
                try:
                    url_validator(file_link)
                
                except ValidationError:
                    self.add_error("file_link", "Некоректне посилання")

            if file_upload:
                cleaned_data['file_upload'] = None

        # Перевірка файлів
        elif file_type == Material.FileTypeChoices.FILE:
            if not file_upload:
                self.add_error("file_upload", "Будь ласка, завантажте файл.")
            
            else:
                ext = os.path.splitext(file_upload.name)[1].lower()
                allowed_extensions = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".zip")

                if ext not in allowed_extensions:
                        self.add_error("file_upload", f"Недозволений формат. Доступні: {', '.join(allowed_extensions)}")

            if file_link:
                cleaned_data['file_link'] = ""

        return cleaned_data