from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail

from .models import User
from .forms import UserRegistrationForm, LoginForm
from product.models import Cart


class UserRegistrationView(View):
    """Handles user registration and cart creation."""

    def get(self, request):
        form = UserRegistrationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            # Create user and corresponding empty cart
            user = User.objects.create_user(**form.cleaned_data)
            Cart.objects.create(user=user)

            # Send welcome email
            send_mail(
                subject='Welcome to Our Platform',
                message='Hi, welcome to our application!',
                from_email='abdulkareemyousaf1245@gmail.com',
                recipient_list=[form.cleaned_data.get('email')],
                fail_silently=True
            )

            return redirect("login")

        return render(request, "register.html", {"form": form})


class UserLoginView(View):
    """Handles user login."""

    def get(self, request):
        form = LoginForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("home")

        return render(request, "login.html", {"form": form})


def logout_view(request):
    """Logs out the user and redirects to login page."""
    logout(request)
    return redirect("login")
