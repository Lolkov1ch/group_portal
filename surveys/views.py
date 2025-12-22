from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Q
from django.utils import timezone
from .models import Survey

# Create your views here.

class SurveysListView(ListView):
    """Список всіх опитувань"""
    model= Survey
    template_name = 'surveys/surveys_list.html'
    context_object_name = 'surveys'
    def get_queryset(self):
        now = timezone.now()

        return Survey.objects.filter(
            is_active=True
        ).filter(
            Q(start_date_lte=now) | Q (start_date__isnull=True)
        ).filters(
            Q(end_date__gte=now) | Q(end_date__isnull=True)
        ).order_by('-start_date', '-create_at')


class SurveyDetailView(DetailView):
    """Деталі конкретного опитування"""
    template_name = 'surveys/survey_detail.html'


class SurveyStepView(TemplateView):
    """Крок опитування"""
    template_name = 'surveys/survey_step.html'

