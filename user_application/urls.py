from django.urls import path
from .views import UserRegistrationView, UserLoginView, logout_view

urlpatterns = [
    path("register/", UserRegistrationView.as_view(), name="register"),
    path("login/", UserLoginView.as_view(), name="login"),
    path("logout/", logout_view, name="logout"),
]
