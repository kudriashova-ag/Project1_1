from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm


def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Реєстрація успішна! Тепер увійдіть до акаунту.')
            return redirect('accounts:login')
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Вітаємо, {user.username}!')
                next_url = request.GET.get('next', '/')
                return redirect(next_url)
            else:
                messages.error(request, 'Неправильне ім\'я користувача або пароль.')
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'Ви вийшли з акаунту.')
    return redirect('/')
