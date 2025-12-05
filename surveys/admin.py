from django.contrib import admin
from .models import Survey, Question, Option, Answer


class QuestionInline(admin.TabularInline):
    """Inline для питань в опитуванні"""
    model = Question
    extra = 1
    fields = ('text', 'question_type', 'order')


class OptionInline(admin.TabularInline):
    """Inline для варіантів відповідей в питанні"""
    model = Option
    extra = 3
    fields = ('text', 'order')


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    """Адмінка для опитувань"""
    list_display = ('title', 'is_active', 'start_date', 'end_date', 'created_by', 'created_at')
    list_filter = ('is_active', 'start_date', 'end_date', 'created_by')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'
    inlines = [QuestionInline]

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Дати', {
            'fields': ('start_date', 'end_date')
        }),
        ('Автор', {
            'fields': ('created_by',)
        }),
    )

    def save_model(self, request, obj, form, change):
        """Автоматично встановлюємо created_by при створенні"""
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Адмінка для питань"""
    list_display = ('text_short', 'survey', 'question_type', 'order', 'created_at')
    list_filter = ('question_type', 'survey', 'created_at')
    search_fields = ('text', 'survey__title')
    inlines = [OptionInline]

    fieldsets = (
        (None, {
            'fields': ('survey', 'text', 'question_type', 'order')
        }),
    )

    def text_short(self, obj):
        """Скорочений текст питання для списку"""
        return obj.text[:50] + '...' if len(obj.text) > 50 else obj.text
    text_short.short_description = 'Текст питання'


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    """Адмінка для варіантів відповідей"""
    list_display = ('text', 'question_short', 'order')
    list_filter = ('question__survey', 'question')
    search_fields = ('text', 'question__text')

    fieldsets = (
        (None, {
            'fields': ('question', 'text', 'order')
        }),
    )

    def question_short(self, obj):
        """Скорочене питання для списку"""
        return obj.question.text[:30] + '...' if len(obj.question.text) > 30 else obj.question.text
    question_short.short_description = 'Питання'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    """Адмінка для відповідей"""
    list_display = ('user', 'survey', 'question_short', 'selected_option', 'text_answer_short', 'created_at')
    list_filter = ('survey', 'question', 'created_at', 'user')
    search_fields = ('user__username', 'text_answer', 'question__text')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Відповідь', {
            'fields': ('user', 'survey', 'question')
        }),
        ('Дані відповіді', {
            'fields': ('selected_option', 'text_answer')
        }),
        ('Метадані', {
            'fields': ('created_at',)
        }),
    )

    def question_short(self, obj):
        """Скорочене питання для списку"""
        return obj.question.text[:30] + '...' if len(obj.question.text) > 30 else obj.question.text
    question_short.short_description = 'Питання'

    def text_answer_short(self, obj):
        """Скорочена текстова відповідь для списку"""
        if obj.text_answer:
            return obj.text_answer[:30] + '...' if len(obj.text_answer) > 30 else obj.text_answer
        return '-'
    text_answer_short.short_description = 'Текстова відповідь'
