from django.urls import path
from .views import GradeListView, GradeCreateView, GradeUpdateView, GradeDeleteView, StudentGradeListView

app_name = "diary"

urlpatterns = [
    path('grades/', GradeListView.as_view(), name='grade_list'),
    path('grades/add/', GradeCreateView.as_view(), name='grade_create'),
    path('grades/<int:pk>/edit/', GradeUpdateView.as_view(), name='grade_update'),
    path('grades/<int:pk>/delete/', GradeDeleteView.as_view(), name='grade_delete'),

    path('my-diary/', StudentGradeListView.as_view(), name='student_grade_list'),
]
