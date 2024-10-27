from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password1', 'password2', 'role')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Username'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Password'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Confirm Password'
            }),
            'role': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
            }),
        }
        error_messages = {
            'username': {
                'required': 'Username is required.',
                'max_length': 'Username must be 150 characters or fewer.',
                'invalid': 'Username can only contain letters, digits and @/./+/-/_ characters.',
            },
            'password1': {
                'required': 'Password is required.',
                'min_length': 'Password must contain at least 8 characters.',
                'password_too_similar': 'Your password can’t be too similar to your other personal information.',
                'password_too_common': 'Your password can’t be a commonly used password.',
                'password_entirely_numeric': 'Your password can’t be entirely numeric.',
            },
            'password2': {
                'required': 'Password confirmation is required.',
                'password_mismatch': 'The two password fields didn’t match.',
            },
        }

class CustomAuthenticationForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'password')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-yellow-500',
                'placeholder': 'Password'
            }),
        }