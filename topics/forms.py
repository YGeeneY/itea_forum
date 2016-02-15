import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm

from topics.models import Topic, Message


class TopicModelForm(forms.ModelForm):

    class Meta:
        model = Topic
        fields = ('name', )
        labels = {
            'name': 'Название темы:'
        }


class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )
        labels = {
            'text': 'Текст сообщения:'
        }


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Логин:')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль:')


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    confirm_terms = forms.BooleanField(
        widget=forms.CheckboxInput(),
        label='Я согласен с правилами',
        error_messages={'required': 'Вы не согласились с правилами'}
    )

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

