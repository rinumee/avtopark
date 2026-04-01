from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class UserRegistrationForm(UserCreationForm):
    phone = forms.CharField(max_length=20, required=True)
    full_name = forms.CharField(max_length=200, required=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'full_name', 'phone', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.phone = self.cleaned_data['phone']
        user.user_type = 'user'
        if commit:
            user.save()
        return user

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Foydalanuvchi nömrə / İstismar',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Parol',
        'class': 'form-control'
    }))