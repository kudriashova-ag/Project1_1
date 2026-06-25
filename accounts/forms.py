from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=20, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'phone_number', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Цей email вже зареєстрований.')
        return email

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        if phone and len(phone) < 7:
            raise forms.ValidationError('Номер телефону занадто короткий.')
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = 'Мінімум 8 символів, не може бути лише цифрами.'
        self.fields['password2'].help_text = 'Введіть той же пароль для перевірки.'


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label='Ім\'я користувача',
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
