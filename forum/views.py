from django.views.generic import ListView
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Category, Topic, Forum, Attachment, ForumSettings, Like, Dislike, Post, Tag
from django.http import HttpResponseForbidden
from .forms import PostForm, TopicForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import UserPassesTestMixin
from .mixins import ModeratorRequiredMixin
from django.views import View
from django.contrib import messages
from django.shortcuts import render
from django.db.models import Prefetch

class CategoryListView(ListView):
    model = Category
    template_name = "forum/category_list.html"
    context_object_name = "categories"
    
    def get_queryset(self):
        return Category.objects.prefetch_related('forums').order_by('name')

class TopicListByCategoryView(ListView):
    model = Topic
    template_name = "forum/topic_list.html"
    context_object_name = "topics"
    paginate_by = 20

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs.get('category_id'))
        queryset = Topic.objects.filter(forum__category=self.category)
    
        tag_slug = self.request.GET.get('tag')
        if tag_slug:
            self.selected_tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=self.selected_tag)
        else:
            self.selected_tag = None
        
        return (
            queryset
            .select_related('author', 'forum')
            .prefetch_related('posts', 'tags')
            .order_by('-is_pinned', '-updated_at')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['all_tags'] = Tag.objects.all()
        context['selected_tag'] = getattr(self, 'selected_tag', None)
        return context

class TopicDetailView(View):
    def get(self, request, pk):
        topic = get_object_or_404(
            Topic.objects.select_related('forum__category', 'author').prefetch_related('tags'), 
            pk=pk
        )
        forum_settings, _ = ForumSettings.objects.get_or_create(pk=1)
        
        posts_prefetch = Prefetch(
            'posts',
            Post.objects.select_related('author').prefetch_related('attachments', 'likes', 'dislikes')
        )
        topic = Topic.objects.prefetch_related(posts_prefetch, 'tags').get(pk=pk)
        posts = topic.posts.all()
        
        form = PostForm()
        return render(request, "forum/topic_detail.html", {
            "topic": topic,
            "posts": posts,
            "reply_form": form,
            "forum_settings": forum_settings,
        })

    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        
        if not request.user.is_authenticated:
            messages.error(request, "Ви повинні увійти, щоб залишити відповідь.")
            return redirect("login")

        if topic.is_locked and not request.user.is_staff:
            messages.error(request, "Тема закрита для нових відповідей.")
            return redirect("forum:topic_detail", pk=topic.pk)

        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.topic = topic
            post.save()

            forum_settings, _ = ForumSettings.objects.get_or_create(pk=1)
            if forum_settings.enable_attachments:
                files = request.FILES.getlist("attachments")
                for f in files:
                    try:
                        attachment = Attachment(post=post, file=f)
                        attachment.full_clean()
                        attachment.save()
                    except Exception as e:
                        messages.warning(request, f"Не вдалося завантажити {f.name}: {str(e)}")

            messages.success(request, "Відповідь успішно створена!")
            return redirect("forum:topic_detail", pk=topic.pk)
        else:
            messages.error(request, "Помилка при створенні відповіді.")
            posts = topic.posts.select_related('author').prefetch_related('attachments', 'likes', 'dislikes').all()
            forum_settings, _ = ForumSettings.objects.get_or_create(pk=1)
            return render(request, "forum/topic_detail.html", {
                "topic": topic,
                "posts": posts,
                "reply_form": form,
                "forum_settings": forum_settings,
            })

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
        
        if not category.is_open:
            messages.error(self.request, "Категорія закрита для створення нових тем.")
            return redirect("forum:topic_list_by_category", category_id=category_id)
        
        forum = category.forums.first()
        if forum is None:
            messages.error(self.request, "Для цієї категорії не існує форуму. Зверніться до адміністратора.")
            return redirect("forum:category_list")
        
        form.instance.forum = forum
        form.instance.author = self.request.user
        topic = form.save()
        
        messages.success(self.request, "Тема успішно створена!")
        return redirect("forum:topic_detail", pk=topic.pk)

class ForumCreateView(LoginRequiredMixin, ModeratorRequiredMixin, CreateView):
    model = Forum
    fields = ['name', 'description', 'category']
    template_name = "forum/forum_create.html"
    success_url = reverse_lazy('forum:category_list')

class TopicUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Topic
    form_class = TopicForm
    template_name = "forum/topic_update.html"
    
    def test_func(self):
        topic = self.get_object()
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return True
        return topic.author == user
    
    def get_success_url(self):
        messages.success(self.request, "Тема успішно оновлена!")
        return reverse_lazy("forum:topic_detail", kwargs={"pk": self.object.pk})
    
    def handle_no_permission(self):
        messages.error(self.request, "У вас немає доступу до цієї дії.")
        return redirect("forum:category_list")

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
        messages.success(self.request, "Тема успішно видалена!")
        return reverse_lazy("forum:topic_list_by_category", kwargs={"category_id": self.object.forum.category_id})
    
    def handle_no_permission(self):
        messages.error(self.request, "У вас немає доступу до цієї дії.")
        return redirect("forum:category_list")

class TogglePinnedView(LoginRequiredMixin, ModeratorRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_pinned = not topic.is_pinned
        topic.save()
        
        if topic.is_pinned:
            messages.success(request, "Тему закріплено!")
        else:
            messages.success(request, "Тему відкріплено!")
        
        return redirect("forum:topic_detail", pk=pk)

class ToggleLockedView(LoginRequiredMixin, ModeratorRequiredMixin, View):
    def post(self, request, pk):
        topic = get_object_or_404(Topic, pk=pk)
        topic.is_locked = not topic.is_locked
        topic.save()
        
        if topic.is_locked:
            messages.success(request, "Тему закрито!")
        else:
            messages.success(request, "Тему відкрито!")
        
        return redirect("forum:topic_detail", pk=pk)

class LikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        forum_settings, _ = ForumSettings.objects.get_or_create(pk=1)

        if not forum_settings.enable_likes:
            messages.error(request, "Лайки вимкнено")
            return redirect("forum:topic_detail", pk=post.topic.pk)

        Dislike.objects.filter(user=request.user, post=post).delete()

        like, created = Like.objects.get_or_create(user=request.user, post=post)
        if not created:
            like.delete()
            messages.info(request, "Лайк знято")
        else:
            messages.success(request, "Лайк додано")

        return redirect("forum:topic_detail", pk=post.topic.pk)


class DislikePostView(LoginRequiredMixin, View):
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        forum_settings, _ = ForumSettings.objects.get_or_create(pk=1)

        if not forum_settings.enable_dislikes:
            messages.error(request, "Дизлайки вимкнено")
            return redirect("forum:topic_detail", pk=post.topic.pk)

        Like.objects.filter(user=request.user, post=post).delete()

        dislike, created = Dislike.objects.get_or_create(user=request.user, post=post)
        if not created:
            dislike.delete()
            messages.info(request, "Дизлайк знято")
        else:
            messages.success(request, "Дизлайк додано")

        return redirect("forum:topic_detail", pk=post.topic.pk)