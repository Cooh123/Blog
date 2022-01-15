from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm, PasswordChangeForm
from . import models
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите Email'})
    )
    username = forms.CharField(
        label='',
        required=True,
        help_text='Нельзя вводить символы: @, /, _',
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Логин'})
    )
   
    password1 = forms.CharField(
        label='',
        required=True,
        help_text='Пароль не должен быть маленьким и простым',
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Пароль'})
    )
    password2 = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Повтарите пароль'})
    )

 
    class Meta:
        model = User
        fields = [ 'username','email', 'password1', 'password2',]

class AuthForm(AuthenticationForm):
    username = forms.CharField(
        label='',
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите логин'})
    )
    password = forms.CharField(
        label='',
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control form-control-lg', 'placeholder': 'Введите пароль'})
    )
    class Meta:
        model = models.User
        fields = ['username', 'password']

class EditPass(PasswordChangeForm):
    old_password = forms.CharField(
        label="Введите старый пароль",
        widget=forms.PasswordInput
        )
    
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput,
        )
    
    new_password2 = forms.CharField(
        label="New password confirmation",
        widget=forms.PasswordInput
        )
    class Meta:
        model = models.Profile
        fields = ['old_password','new_password1','new_password2']

class UpdateUserForm(forms.ModelForm):
    class Meta:
        username = forms.CharField(
            label='хехе'
        )
        model = User
        fields = ['username','first_name','last_name','email']


class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['mobile_number', 'bio', 'img']

