from django.shortcuts import render
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """Головна сторінка порталу"""
    template_name = 'core/home.html'
