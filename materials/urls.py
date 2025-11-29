from django.urls import path
from .views import CreateMaterial

app_name = "materials"

urlpatterns = [
    path("create/", CreateMaterial.as_view(), name="material_create")
]