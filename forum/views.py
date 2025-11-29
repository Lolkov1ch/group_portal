from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Topic, Post, Forum
from .forms import PostForm, TopicForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from django.utils import timezone
from .mixins import ModeratorRequiredMixin
from django.views import View

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
        context["posts"] = self.object.posts.all().order_by("created_at")
        context["reply_form"] = PostForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not request.user.is_authenticated:
            return redirect("login")
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.topic = self.object
            post.save()
        return redirect("forum:topic_detail", pk=self.object.pk)
    

class TopicCreateView(LoginRequiredMixin, CreateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/topic_create.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_id'] = self.kwargs.get('category_id')
        return context
    
    def form_valid(self, form):
        category_id = self.kwargs.get("category_id")
        category = get_object_or_404(Category, id=category_id)
        forum = category.forums.first() 
        form.instance.forum = forum
        form.instance.author = self.request.user
        topic = form.save()
        
        return redirect("forum:topic_detail", pk=topic.pk)

class ForumCreateView(LoginRequiredMixin, ModeratorRequiredMixin, CreateView):
    model = Forum
    fields = ['name', 'description', 'category']
    template_name = "forum/forum_create.html"
    success_url = reverse_lazy('forum:category_list')

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/topic_create.html"
    
    def test_func(self):
        topic = self.get_object()
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        return topic.author == user
    
    def get_success_url(self):
        return reverse_lazy("forum:topic_detail", kwargs={"pk": self.object.pk})
    
    def handle_no_permission(self):
        return redirect("no_access")

class TopicDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Topic
    template_name = "forum/topic_delete.html"
    
    def test_func(self):
        topic = self.get_object()
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        return topic.author == user
    
    def get_success_url(self):
        return reverse_lazy("forum:topic_list_by_category", kwargs={"category_id": self.object.forum.category_id})
    

class TogglePinnedView(LoginRequiredMixin, ModeratorRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_pinned = not topic.is_pinned
        topic.save()
        return redirect("forum:topic_detail", pk=pk)


class ToggleLockedView(LoginRequiredMixin, ModeratorRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_locked = not topic.is_locked
        topic.save()
        return redirect("forum:topic_detail", pk=pk)