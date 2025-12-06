from django.contrib import admin
from .models import Announcement

# Register your models here.

@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published_date", "is_important")
    list_filter = ("is_important", "published_date")
    search_fields = ("title", "text", "author__username")
