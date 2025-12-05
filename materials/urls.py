from django.urls import path
from .views import CreateMaterial, ListMaterial, DetailMaterial

app_name = "materials"

urlpatterns = [
    path("create/", CreateMaterial.as_view(), name="material_create"),
    path("", ListMaterial.as_view(), name="material_list"),
    path("<int:pk>/", DetailMaterial.as_view(), name="material_detail")
]