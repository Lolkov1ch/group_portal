from django.contrib import admin
from django.utils.html import format_html
from .models import MediaItem


class MediaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'media_type', 'is_approved', 'created_at', 'thumbnail_preview')
    list_filter = ('is_approved', 'media_type', 'created_at')
    search_fields = ('title', 'description', 'game_name', 'author__username')
    list_editable = ('is_approved',)
    readonly_fields = ('created_at', 'updated_at', 'file_preview')
    
    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'description', 'author')
        }),
        ('Медіа', {
            'fields': ('file', 'file_preview', 'media_type')
        }),
        ('Додаткова інформація', {
            'fields': ('game_name', 'is_approved')
        }),
        ('Дати', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['approve_items', 'reject_items']
    
    def thumbnail_preview(self, obj):
        if obj.is_image():
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;" />',
                obj.file.url
            )
        return '📹 Відео'
    thumbnail_preview.short_description = 'Превʼю'
    
    def file_preview(self, obj):
        if not obj.file:
            return "Немає файлу"
        
        if obj.is_image():
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 500px;" />',
                obj.file.url
            )
        else:
            return format_html(
                '<video controls style="max-width: 500px;"><source src="{}"></video>',
                obj.file.url
            )
    file_preview.short_description = 'Перегляд файлу'
    
    def approve_items(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'Схвалено {updated} медіафайл(ів).')
    approve_items.short_description = 'Схвалити вибрані медіафайли'
    
    def reject_items(self, request, queryset):
        count = queryset.count()
        queryset.delete()
        self.message_user(request, f'Видалено {count} медіафайл(ів).')
    reject_items.short_description = 'Видалити вибрані медіафайли'


admin.site.register(MediaItem, MediaItemAdmin)