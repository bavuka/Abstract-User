from django import forms
from app1.models import User
from django.contrib.auth.forms import UserCreationForm

class UserRegistration(UserCreationForm):
    class Meta:
        model=User
        fields=["username","email","phone","password1","password2"]


class UserLogin(UserCreationForm):
    class Meta:
        model=User
        fields=["username","password1"]        