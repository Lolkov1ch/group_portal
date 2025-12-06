from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .views import * 

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='registration/logged_out.html'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/<int:pk>', UserDetailView.as_view(), name='user_details'),
]