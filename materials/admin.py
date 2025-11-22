from django.contrib import admin
from .models import Material

# Register your models here.
@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("name", "file_type", "file_link", "subject", "author", "created_at")
    list_filter = ("file_type",)
    search_fields = ("name", "author__username")
    readonly_fields = ("created_at",)
