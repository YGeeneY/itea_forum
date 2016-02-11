from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from topics.forms import LoginForm, RegisterForm


def logout_view(request):
    logout(request)
    return redirect('/topics/login')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        error = False

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/topics/index')
                else:
                    error = 'Данный аккуант заблокирован'
            else:
                error = 'Пользователя с таким именем не существует, либо пароль не верный'
        return render(request, 'log_in.html', {'form': form, 'error': error})

    elif request.method == 'GET':
        logout(request)
        return render(request, 'log_in.html', {'form': LoginForm})


def register_view(request):
    if request.method == 'GET':
        logout(request)
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = User.objects.create_user(username=username, email=email, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('/topics/index')

        else:
            return render(request, 'register.html', {'form': form})