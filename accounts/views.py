from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView

# Create your views here.

class RegisterView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = '/' 
    
    def form_valid(self, form):
        responce = super().form_valid(form)
        login(self.request, self.object)
        return responce
       