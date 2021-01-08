from django.shortcuts import render
from .forms import UserRegiserForm, UserLoginForm
from django.contrib import messages
from django.contrib.auth import login, logout
from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.


def home(request):
    return render(request, 'auth_app/home.html')


def register(request):
    if request.method == 'POST':
        form = UserRegiserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегистрировались! Залогиньтесь: ')
            return redirect('/messenger_app/')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegiserForm()
    return render(request, 'auth_app/register.html', {"form": form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('/messenger_app/')
    else:
        form = UserLoginForm()
    return render(request, 'auth_app/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')