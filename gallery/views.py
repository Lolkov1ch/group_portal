from django.views.generic import ListView, DetailView
from .models import MediaItem


class GalleryListView(ListView):
    model = MediaItem
    template_name = 'gallery/gallery_list.html'
    context_object_name = 'items'
    ordering = ['-created_at']

    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=True).order_by('-created_at')


class GalleryDetailView(DetailView):
    model = MediaItem
    template_name = 'gallery/gallery_detail.html'
    context_object_name = 'item'

    def get_queryset(self):
        return MediaItem.objects.filter(is_approved=True)
