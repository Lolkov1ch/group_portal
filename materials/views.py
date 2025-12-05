from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Material, MaterialCategory
from .forms import MaterialCreateForm
from django.http import HttpResponseRedirect
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
        if self.request.user.is_authenticated:
            return super().handle_no_permission()  # 403
        return redirect("login")

    # Перевірка валідності форми
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    

class ListMaterial(ListView):
    model = Material
    template_name = "materials/material_list.html"
    context_object_name = "materials"
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        # Якщо немає поточних GET-фільтрів, але є збережені в сесії — редірект з ними
        if not (request.GET.get('category') or request.GET.get('engine') or request.GET.get('type')):
            filters = request.session.get("material_filters")
            if filters and (filters.get("category") or filters.get("engine") or filters.get("type")):
                params = []
                if filters.get("category"):
                    params.append(f"category={filters['category']}")
                if filters.get("engine"):
                    params.append(f"engine={filters['engine']}")
                if filters.get("type"):
                    params.append(f"type={filters['type']}")
                redirect_url = f"{reverse_lazy('material_list')}?{'&'.join(params)}"
                return HttpResponseRedirect(redirect_url)

        return super().get(request, *args, **kwargs)
    

    def get_queryset(self):
         # Показувати лише опубліковані матеріали
        queryset = Material.objects.filter(is_published=Material.IsPublishedChoices.PUBLISHED)

        category_id = self.request.GET.get('category')
        engine = self.request.GET.get('engine')
        file_type = self.request.GET.get('type')

        # Фільтри
        if category_id:
            queryset = queryset.filter(category__id=category_id)

        if engine:
            queryset = queryset.filter(engine=engine)

        if file_type:
            queryset = queryset.filter(file_type=file_type)

        # Збереження фільтрів у сесії
        if category_id or engine or file_type:
            self.request.session["material_filters"] = {
                "category": category_id,
                "engine": engine,
                "type": file_type,
            }
        
        elif "material_filters" in self.request.session:
            del self.request.session["material_filters"] # Видалення збережених фільтрів

        return queryset
    
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["categories"] = MaterialCategory.objects.all()
        context["engines"] = Material.EngineChoices.choices
        context["file_types"] = Material.FileTypeChoices.choices

        context['active_category'] = self.request.GET.get('category')
        context['active_engine'] = self.request.GET.get('engine')
        context['active_type'] = self.request.GET.get('type')

        get_params = self.request.GET.copy()
        if 'page' in get_params:
            del get_params['page']
        context['get_params_except_page'] = get_params.urlencode()
        
        return context


class DetailMaterial(DetailView):
    model = Material
    template_name = "materials/material_detail.html"
    context_object_name = "material"
