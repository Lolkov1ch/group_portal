from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import Category, Topic

class CategoryListView(ListView):
    model = Category
    template_name = 'forum/category_list.html'
    context_object_name = 'categories'

class TopicListByCategoryView(ListView):
    model = Topic
    template_name = 'forum/topic_list.html'
    context_object_name = 'topics'

    def get_queryset(self):
        category_id = self.kwargs.get('category_id')
        self.category = get_object_or_404(Category, pk=category_id)
        return Topic.objects.filter(forum__category=self.category).select_related('author', 'forum')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context
