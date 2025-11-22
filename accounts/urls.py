from django.urls import path

from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', MainMenuView.as_view(), name='main_menu'),
    # path('login/', RegisterView.as_view(), name='login'),
    # path('register/', LoginView.as_view(), name='register'),
]