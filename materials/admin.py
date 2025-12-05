from django.contrib import admin
from .models import Material, MaterialCategory

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "file_type", "category", "engine", "author", "created_at")
    list_filter = ("file_type", "category__title")
    search_fields = ("title", "author__username")
    readonly_fields = ("created_at",)


admin.site.register(MaterialCategory)
