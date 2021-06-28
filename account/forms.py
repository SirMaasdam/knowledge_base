from django import forms
from django.contrib.auth.forms import AuthenticationForm, UsernameField, UserCreationForm
from django.contrib.auth.models import User


class AccountAuthenticationForm(AuthenticationForm):
    username = UsernameField(label='Логин или email адрес',
                             widget=forms.TextInput(attrs={'autofocus': True,
                                                           'class': 'uk-input uk-border-rounded'}))
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'current-password',
                                          'class': 'uk-input uk-border-rounded'}),
    )


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label='Пароль',
                               strip=False,
                               widget=forms.PasswordInput(attrs={'class': 'uk-input uk-border-rounded'}))
    password2 = forms.CharField(label='Повторите пароль',
                                strip=False,
                                widget=forms.PasswordInput(attrs={'class': 'uk-input uk-border-rounded'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
        help_texts = {
            'username': None,
        }
        labels = {
            'username': 'Логин:',
            'email': 'email-адрес'
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'uk-input uk-border-rounded'}),
            'email': forms.TextInput(attrs={'class': 'uk-input uk-border-rounded'})
        }
