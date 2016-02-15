from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import redirect

from django.views.generic import FormView

from topics.forms import UserCreateForm


def logout_view(request):
    logout(request)
    return redirect('/topics/login')


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'log_in.html'
    success_url = '/topics/index'


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
