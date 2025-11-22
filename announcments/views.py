from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Announcement

# Create your views here.

class AnnouncementListView(ListView):
    model = Announcement
    template_name = 'announcements/announcement_list.html'
    context_object_name = 'announcements'

class AnnouncementCreateView(CreateView):
    model = Announcement
    fields = ['title', 'text', 'image', 'is_active']
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcements:list')

class AnnouncementUpdateView(UpdateView):
    model = Announcement
    fields = ['title', 'text', 'image', 'is_active']
    template_name = 'announcements/announcement_form.html'
    success_url = reverse_lazy('announcements:list')


class AnnouncementDeleteView(DeleteView):
    model = Announcement
    template_name = 'announcements/announcement_confirm_delete.html'
    success_url = reverse_lazy('announcements:list')