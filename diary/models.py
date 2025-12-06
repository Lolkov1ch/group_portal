from django.db import models
from django.contrib.auth.models import User

class Subject(models.Model):
    name = models.CharField(max_length=100,
                            unique=True,
                            verbose_name="Назва предмету"
    )
    
    description = models.TextField(blank=True,
                                   verbose_name="Опис"
    )
    
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Предмет"
        verbose_name_plural = "Предмети"


class Grade(models.Model):
    student = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='grades',
                                verbose_name="Учень"
    )
    
    subject = models.ForeignKey(Subject,
                                on_delete=models.CASCADE,
                                related_name='grades',
                                verbose_name="Предмет"
    )

    score = models.PositiveIntegerField(verbose_name="Оцінка/Бал")

    comment = models.TextField(verbose_name="Коментар")
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name="Дата виставлення"
    )
    
    teacher = models.ForeignKey(User,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='given_grades',
                                verbose_name="Викладач"
    )

    def __str__(self):
        return f"{self.student} - {self.subject}: {self.score}"

    class Meta:
        verbose_name = "Оцінка"
        verbose_name_plural = "Оцінки"
        ordering = ['-created_at']