from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = "forum"

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('forum/create/', views.ForumCreateView.as_view(), name='forum_create'),
    path('category/<int:category_id>/', views.TopicListByCategoryView.as_view(), name='topic_list_by_category'),
    path('category/<int:category_id>/topic/create/', views.TopicCreateView.as_view(), name='topic_create'),
    path('topic/<int:pk>/', views.TopicDetailView.as_view(), name='topic_detail'),
    path('topic/<int:pk>/edit/', views.TopicUpdateView.as_view(), name='topic_update'),
    path('topic/<int:pk>/delete/', views.TopicDeleteView.as_view(), name='topic_delete'),
    path("topic/<int:pk>/pin/", views.TogglePinnedView.as_view(), name="toggle_pin"),
    path("topic/<int:pk>/lock/", views.ToggleLockedView.as_view(), name="toggle_lock"),
    path("post/<int:pk>/like/", views.LikePostView.as_view(), name="like_post"),
    path("post/<int:pk>/dislike/", views.DislikePostView.as_view(), name="dislike_post"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)