from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', MainMenuView.as_view(), name='main_menu'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
]