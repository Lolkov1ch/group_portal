from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.

class Announcement(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    text = models.TextField(verbose_name="Текст")
    published_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публікації")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Автор")
    is_important = models.BooleanField(default=False, verbose_name="Важливе")

    class Meta:
        verbose_name = "Оголошення"
        verbose_name_plural = "Оголошення"
        ordering = ['-published_date']

    def __str__(self):
        return f"{self.title} ({'Важливе' if self.is_important else 'Звичайне'})"

    def short_text(self):
        return self.text[:50] + "..." if len(self.text) > 50 else self.text