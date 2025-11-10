from django.contrib.auth.forms import (AuthenticationForm, UserCreationForm, 
                                       UserChangeForm)
from django import forms

from users.models import User


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'autofocus': True,
                                          'class': 'form-control',
                                          'placeholder': 'Введите имя пользователя'}))
    password = forms.CharField(label='Пароль',
                               strip=False,
                               widget=forms.PasswordInput(
                                   attrs={'autocomplete': 'current-password',
                                          'class': 'form-control',
                                          'placeholder': 'Введите пароль'}))

    class Meta:
        model = User
        fields = ('username', 'password')


class UserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя*',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия*',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Введите фамилию'}))
    username = forms.CharField(label='Имя пользователя*',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(label='Email*',
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Введите email *youremail@example.com'}))
    password1 = forms.CharField(label='Пароль*',
                                strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'current-password',
                                           'class': 'form-control',
                                           'placeholder': 'Введите пароль'}))
    password2 = forms.CharField(label='Подтверждение пароля*',
                                strip=False,
                                widget=forms.PasswordInput(
                                    attrs={'autocomplete': 'current-password',
                                           'class': 'form-control',
                                           'placeholder': 'Подтвердите пароль'}))

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2"
        )


class UserProfileForm(UserChangeForm):
    image = forms.ImageField(required=False,
                             widget=forms.FileInput(
                                 attrs={'class': 'form-control mt-3',
                                        'accept': 'image/*'}))
    first_name = forms.CharField(label='Имя',
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='Фамилия',
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control',
                                           'placeholder': 'Введите фамилию'}))
    username = forms.CharField(label='Имя пользователя',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': 'Введите имя пользователя'}))
    email = forms.CharField(label='Email',
                            widget=forms.EmailInput(
                                attrs={'class': 'form-control',
                                       'placeholder': 'Введите email *youremail@example.com'}))

    class Meta:
        model = User
        fields = (
            'image',
            'first_name',
            'last_name',
            'username',
            'email'
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'password' in self.fields:
            del self.fields['password']