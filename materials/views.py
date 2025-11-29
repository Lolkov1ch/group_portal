from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Material
from .forms import MaterialCreateForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

class CreateMaterial(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Material
    form_class = MaterialCreateForm
    template_name = "materials/create_material.html"
    success_url = reverse_lazy("material_list")

    # Перевірка чи належить користувач до групи (UserPassesTestMixin)
    def test_func(self):
        user = self.request.user
        is_teacher = user.groups.filter(name="Teachers").exists() # За необхідності змінити на необхідну групу
        return user.is_staff or is_teacher
    
    # Якщо користувач не має прав
    def handle_no_permission(self):
        return redirect("login")

    # Перевірка валідності форми
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
