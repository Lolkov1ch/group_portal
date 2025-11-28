from django import forms
from .models import Material
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError

class MaterialCreateForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = [
            "name", "description", "file_type", "file_link", "subject", "author"
        ]
    
    # Перевірка форми
    def clean(self):
        cleaned_data = super().clean() # Очищення даних

        file_type = cleaned_data.get('file_type')
        file_link = cleaned_data.get('file_link')

        if not file_type or not file_link:
            return cleaned_data

        if file_type in [Material.FileTypeChoices.LINK, Material.FileTypeChoices.VIDEO]:
            url_validator = URLValidator()
            try:
                url_validator(file_link)
            
            except ValidationError:
                self.add_error("file_link", "Incorrect URL")

        elif file_type == Material.FileTypeChoices.FILE:
            allowed_extensions = (".pdf", ".doc", ".docx", ".ppt", ".pptx", ".zip")

            if not file_link.lower().endswith(allowed_extensions):
                self.add_error(f"file_link", "Invalid file extension. Allowed: {', '.join(allowed_extension)}")

        return cleaned_data