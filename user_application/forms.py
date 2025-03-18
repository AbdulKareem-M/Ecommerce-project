from django import forms
from .models import User


class UserRegistrationForm(forms.ModelForm):

    class Meta:
        model=User

        fields=["username","first_name","last_name","password","email"]


class LoginForm(forms.Form):

    username=forms.CharField(max_length=100)

    password=forms.CharField(max_length=100,widget=forms.PasswordInput())