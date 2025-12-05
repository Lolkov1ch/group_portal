from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Survey(models.Model):
    """Модель опитування"""
    title = models.CharField(max_length=255, verbose_name="Назва")
    description = models.TextField(verbose_name="Опис", blank=True)
    is_active = models.BooleanField(default=True, verbose_name="Активне")
    start_date = models.DateTimeField(verbose_name="Дата початку")
    end_date = models.DateTimeField(verbose_name="Дата завершення", null=True, blank=True)
    created_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_surveys',
        verbose_name="Створив"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")

    class Meta:
        verbose_name = "Опитування"
        verbose_name_plural = "Опитування"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Question(models.Model):
    """Модель питання"""
    QUESTION_TYPES = (
        ('single', 'Одна відповідь'),
        ('multi', 'Множинний вибір'),
        ('text', 'Текстова відповідь'),
    )

    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Опитування"
    )
    text = models.TextField(verbose_name="Текст питання")
    question_type = models.CharField(
        max_length=10,
        choices=QUESTION_TYPES,
        default='single',
        verbose_name="Тип питання"
    )
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    class Meta:
        verbose_name = "Питання"
        verbose_name_plural = "Питання"
        ordering = ['survey', 'order']

    def __str__(self):
        return f"{self.survey.title} - {self.text[:50]}"


class Option(models.Model):
    """Модель варіанту відповіді"""
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='options',
        verbose_name="Питання"
    )
    text = models.CharField(max_length=255, verbose_name="Текст варіанту")
    order = models.PositiveIntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name="Порядок"
    )

    class Meta:
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповідей"
        ordering = ['question', 'order']

    def __str__(self):
        return f"{self.question.text[:30]} - {self.text}"


class Answer(models.Model):
    """Модель відповіді користувача"""
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='survey_answers',
        verbose_name="Користувач"
    )
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Опитування"
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name="Питання"
    )
    selected_option = models.ForeignKey(
        Option,
        on_delete=models.CASCADE,
        related_name='answers',
        null=True,
        blank=True,
        verbose_name="Обраний варіант"
    )
    text_answer = models.TextField(
        blank=True,
        verbose_name="Текстова відповідь"
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата відповіді")

    class Meta:
        verbose_name = "Відповідь"
        verbose_name_plural = "Відповіді"
        ordering = ['-created_at']
        # Унікальність для запобігання дублюванню відповідей (крім multi choice)
        unique_together = ['user', 'question', 'selected_option']

    def __str__(self):
        return f"{self.user.username} - {self.question.text[:30]}"
