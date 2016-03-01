from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404

from django.views.generic import FormView, DetailView, TemplateView

from topics.forms import UserCreateForm

from .models import UserDetails, UserMessages


def logout_view(request):
    logout(request)
    messages.info(request, 'Вы успешно вышли!' )
    return redirect(
        reverse_lazy('login')
    )


class LoginView(FormView):
    form_class = AuthenticationForm
    template_name = 'landing/login.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        login(self.request, user)
        messages.info(self.request, 'Вы успешно вошли под аккаунтом  %s!' % (username,))

        # hint to get back on requested page.
        self.success_url = self.request.GET.get('next', False) or self.success_url
        
        return super(LoginView, self).form_valid(form)


class RegisterView(FormView):
    form_class = UserCreateForm
    template_name = 'landing/register.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password1']
        User.objects.create_user(username=username, email=email, password=password)
        user = authenticate(username=username, password=password)

        UserDetails.objects.create(user=user)

        login(self.request, user)

        messages.info(self.request, 'Аккаунт %s успешно создан!' % (username,))
        return super(RegisterView, self).form_valid(form)


class AccountView(DetailView):
    model = User
    template_name = 'landing/account.html'
    slug_field = 'username'
    context_object_name = 'user_profile'


class SelfAccountView(TemplateView):
    template_name = 'landing/account.html'

    def get_context_data(self, **kwargs):
        context = super(SelfAccountView, self).get_context_data()
        user = self.request.user
        context['user_profile'] = user
        return context


class InboxView(TemplateView):
    template_name = 'landing/inbox.html'

    def get_context_data(self, **kwargs):
        context = super(InboxView, self).get_context_data()
        user = self.request.user
        context['user_profile'] = UserMessages.objects.filter(receiver=user)
        return context


class InboxDetailView(DetailView):
    model = UserMessages
    template_name = 'landing/inbox_detail.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)