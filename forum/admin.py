from django.contrib import admin
from .models import Category, Forum, Topic, Post, Attachment, Like, Dislike, ForumSettings, Tag

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'color']
    prepopulated_fields = {'slug': ('name',)}

admin.site.register(Category)
admin.site.register(Forum)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(Attachment)
admin.site.register(Like)
admin.site.register(Dislike)
admin.site.register(ForumSettings)