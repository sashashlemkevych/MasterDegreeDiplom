# recommendations/forms.py

from django import forms # type: ignore
from django.contrib.auth.models import User # type: ignore
from django.forms import ModelForm  # type: ignore


class RegisterForm(ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']
        
