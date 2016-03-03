from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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