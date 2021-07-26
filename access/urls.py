from django.urls import path

from django.contrib.auth.views import LoginView, LogoutView
from .views import UserCreateView

urlpatterns = [
    path('login', LoginView.as_view(template_name='access/login.html'),name='login'),
    path('logout', LogoutView.as_view(next_page='index'), name='logout'),
    path('newuser', UserCreateView.as_view(), name='newuser'),
]
