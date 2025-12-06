from django.urls import path
from .views import (
    GalleryListView, 
    GalleryDetailView,
    MediaItemCreateView,
    ModerationListView,
    ApproveMediaView,
    RejectMediaView,
    DeleteMediaView
)

app_name = 'gallery'

urlpatterns = [
    path('', GalleryListView.as_view(), name='list'),
    path('create/', MediaItemCreateView.as_view(), name='create'),
    path('<int:pk>/', GalleryDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/', DeleteMediaView.as_view(), name='delete'),
    
    path('moderation/', ModerationListView.as_view(), name='moderation'),
    path('moderation/<int:pk>/approve/', ApproveMediaView.as_view(), name='approve'),
    path('moderation/<int:pk>/reject/', RejectMediaView.as_view(), name='reject'),
]