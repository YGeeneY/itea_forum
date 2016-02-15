from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from django.views.generic import FormView

from topics.forms import LoginForm, UserCreateForm


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


class RegisterView(FormView):
    form_class = UserCreateForm
    template_name = 'register.html'
    success_url = '/topics/index'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(RegisterView, self).form_valid(form)
