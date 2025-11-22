from django.urls import path
from . import views

app_name = 'forum'

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('category/<int:category_id>/', views.TopicListByCategoryView.as_view(), name='topic_list_by_category'),
]
