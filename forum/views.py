from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import MediaItem
from .forms import MediaItemForm
from .mixins import ModeratorRequiredMixin
from django.db.models import Q


class GalleryListView(ListView):
    model = MediaItem
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'items'
    paginate_by = 12

    def get_queryset(self):
        queryset = MediaItem.objects.filter(
            is_approved=True
        ).select_related('author')
        
        media_type = self.request.GET.get('type')
        if media_type and media_type in [choice[0] for choice in MediaItem.MEDIA_TYPES]:
            queryset = queryset.filter(media_type=media_type)
        
        game = self.request.GET.get('game')
        if game:
            queryset = queryset.filter(game_name__iexact=game)
        
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | 
                Q(game_name__icontains=search) |
                Q(description__icontains=search)
            )
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['media_types'] = MediaItem.MEDIA_TYPES
        context['current_type'] = self.request.GET.get('type', '')
        context['search_query'] = self.request.GET.get('search', '')
        context['current_game'] = self.request.GET.get('game', '')
        
        context['games'] = MediaItem.objects.filter(
            is_approved=True,
            game_name__isnull=False
        ).exclude(
            game_name=''
        ).values_list('game_name', flat=True).distinct().order_by('game_name')
        
        context['total_items'] = self.get_queryset().count()
        
        return context


class GalleryDetailView(DetailView):
    model = MediaItem
    template_name = 'gallery/gallery_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=True)


class MediaItemCreateView(LoginRequiredMixin, CreateView):
    model = MediaItem
    form_class = MediaItemForm
    template_name = 'gallery/mediaitem_create.html'
    success_url = reverse_lazy('gallery:list')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.is_approved = False
        
        response = super().form_valid(form)
        
        messages.success(
            self.request,
            'Ваш скрін буде опубліковано після перевірки модератором.'
        )
        
        return response
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            'Будь ласка, виправте помилки у формі.'
        )
        return super().form_invalid(form)


class ModerationListView(ModeratorRequiredMixin, ListView):
    model = MediaItem
    template_name = 'gallery/moderation_list.html'
    context_object_name = 'items'
    paginate_by = 20

    def get_queryset(self):
        return MediaItem.objects.filter(
            is_approved=False
        ).select_related('author').order_by('-created_at')


class ApproveMediaView(ModeratorRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(MediaItem, pk=pk)
        item.is_approved = True
        item.save()
        
        messages.success(
            request,
            f'Медіафайл "{item.title}" схвалено.'
        )
        
        return redirect('gallery:moderation')


class RejectMediaView(ModeratorRequiredMixin, View):
    def post(self, request, pk):
        item = get_object_or_404(MediaItem, pk=pk)
        
        title = item.title
        author = item.author.username if item.author else "Анонім"
        
        item.delete()
        
        messages.warning(
            request,
            f'Медіафайл "{title}" (автор: {author}) відхилено та видалено.'
        )
        
        return redirect('gallery:moderation')


class DeleteMediaView(LoginRequiredMixin, View):
    def get(self, request, pk):
        item = get_object_or_404(MediaItem, pk=pk)
        
        if item.author != request.user and not request.user.is_staff:
            messages.error(request, 'У вас немає прав видалити цей файл.')
            return redirect('gallery:detail', pk=pk)
        
        title = item.title
        item.delete()
        
        messages.success(request, f'Медіафайл "{title}" видалено.')
        return redirect('gallery:list')
    
    def post(self, request, pk):
        return self.get(request, pk)