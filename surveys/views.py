from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.

class SurveysListView(TemplateView):
    """Список всіх опитувань"""
    template_name = 'surveys/surveys_list.html'


class SurveyDetailView(TemplateView):
    """Деталі конкретного опитування"""
    template_name = 'surveys/survey_detail.html'


class SurveyStepView(TemplateView):
    """Крок опитування"""
    template_name = 'surveys/survey_step.html'
