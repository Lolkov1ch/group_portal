from django.urls import path
from . import views

app_name = 'surveys'

urlpatterns = [
    path('', views.SurveysListView.as_view(), name='list'),
    path('<int:pk>/', views.SurveyDetailView.as_view(), name='detail'),
    path('<int:pk>/step/<int:step>/', views.SurveyStepView.as_view(), name='step'),
]
