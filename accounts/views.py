from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import redirect

from django.views.generic import FormView

from topics.forms import UserCreateForm


def logout_view(request):
    logout(request)
    return redirect(
        reverse_lazy('login')
    )


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'landing/login.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(LoginView, self).form_valid(form)


class RegisterView(FormView):
    form_class = UserCreateForm
    template_name = 'landing/register.html'
    success_url = reverse_lazy('main')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(username=username, password=password)
        login(self.request, user)

        return super(RegisterView, self).form_valid(form)