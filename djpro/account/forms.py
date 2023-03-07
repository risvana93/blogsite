from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    class Meta():
        model=User
        fields=['first_name','last_name','email','username','password1','password2']

class SignInForm(forms.Form):
    username=forms.CharField(max_length=120)  
    password=forms.CharField(max_length=120,widget=forms.PasswordInput())      