from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Topic, Post
from .forms import PostForm

class CategoryListView(ListView):
    model = Category
    template_name = "forum/category_list.html"
    context_object_name = "categories"

class TopicListByCategoryView(ListView):
    model = Topic
    template_name = "forum/topic_list.html"
    context_object_name = "topics"

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        return Topic.objects.filter(forum__category=self.category).select_related('author', 'forum')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

class TopicDetailView(DetailView):
    model = Topic
    template_name = "forum/topic_detail.html"
    context_object_name = "topic"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["posts"] = self.object.posts.select_related("author").order_by("created_at")
        if self.request.user.is_authenticated:
            context["form"] = PostForm()
        return context
