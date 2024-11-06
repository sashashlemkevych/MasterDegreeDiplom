# recommendations/forms.py

from django import forms # type: ignore
from django.contrib.auth.models import User # type: ignore
from .models import Movie
from django.forms import ModelForm, TextInput, DateInput, ClearableFileInput, Textarea, DateInput, DateField, ImageField# type: ignore


class RegisterForm(ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Підтвердження пароля', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'password', 'password_confirm', 'email']


class AddMovieForm(ModelForm):
    class Meta:
        model = Movie
        fields = ['title', 'genres', 'overview', 'release_date', 'image']
        widgets = {
            "title": TextInput(attrs={
                'class': 'form-control',
            }),
            "genres": TextInput(attrs={
                'class': 'form-control',
            }),
            "overview": Textarea(attrs={
                'class': 'form-control',
            }),
            "release_date": DateInput(attrs={
                'type' : 'date',
                'class': 'form-select',
            }),
            "image": ClearableFileInput(attrs={
                'class': 'form-control',
            }),
        }
