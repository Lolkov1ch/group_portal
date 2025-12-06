from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView, DetailView, UpdateView

from .models import *
from .mixins import *
from .forms import *
# Create your views here.

class UserDetailView(DetailView):
    model = ProfileModel
    context_object_name = 'user'
    template_name = 'profile/profile_view.html'

class UserUpdateView(LoginRequiredMixin, AbleToUpdateMixin, UpdateView):
    models = ProfileModel
    form = UserForm
    pass

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/' 
    
    def form_valid(self, form):
        responce = super().form_valid(form)
        login(self.request, self.object)
        return responce