from django.contrib import admin
from .models import Subject, Grade

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'subject', 'score', 'created_at', 'teacher')
    list_filter = ('subject', 'created_at', 'student')
    search_fields = ('student__username', 'comment')
    readonly_fields = ('created_at',)