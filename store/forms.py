from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 

class CustomUserForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control my-2',
            'placeholder': 'Enter a Username'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control my-2',
            'placeholder': 'Enter an Email'
        })
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-2',
            'placeholder': 'Enter Your Password'
        })
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control my-2',
            'placeholder': 'Re-enter Your Password'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
