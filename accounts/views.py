from django.shortcuts import get_object_or_404, redirect, render
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView, UpdateView, CreateView

from .models import *
# Create your views here.

class MainMenuView(ListView):
    model = ProfileModel
    template_name = 'main_menu.html'
    context_object_name = 'main_menu'


class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('registration:login')
    
    def form_valid(self, form):
        responce = super().form_valid(form)
        login(self.request, self.object)
        return responce
       