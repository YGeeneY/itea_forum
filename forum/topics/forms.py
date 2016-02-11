import re
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class TopicForm(forms.Form):
    name = forms.CharField(label='Название', max_length=1000, widget=forms.TextInput(
        attrs={'class': "form-control", 'placeholder': "Название темы"}
    ))

    def clean_name(self):
        name = self.cleaned_data['name']
        if '?' in name:
            raise ValidationError("Знак вопроса недопустим")
        return name


class MessageForm(forms.Form):
    text = forms.CharField(widget=forms.Textarea(
        attrs={'class': "form-control",
               'id': 'markItUp',
               'style': 'resize: none; padding-bottom: 45px;',
               'placeholder': "Текст сообщения"
               }
    ))


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Логин:')

    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль:')


class RegisterForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(), label='Логин:')
    email = forms.CharField(widget=forms.EmailInput(), label='Email:')
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль:')
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Подтвердить пароль:')
    confirm_terms = forms.BooleanField(
        widget=forms.CheckboxInput,
        label='Я согласен с правилами',
        error_messages={'required': 'Вы не согласились с правилами'}
    )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data['confirm_password']
        password = self.cleaned_data['password']

        if confirm_password == password:
            return confirm_password
        else:
            raise ValidationError('Пароли не совпадают')

    def clean_username(self):
        new_user = self.cleaned_data['username']
        if len(new_user) < 6:
            raise ValidationError('Логин должен быть больше 6ти символов')

        pattern = re.compile(r'[A-Za-z0-9_.]+')

        if not re.match(pattern, new_user):
            raise ValidationError('Только латинские символы допустимы')

        try:
            User.objects.get(username=new_user)
            raise ValidationError('Пользователь с таким именем уже существует')

        except User.DoesNotExist:
            return new_user

    def clean_password(self):
        password = self.cleaned_data['password']
        print(password, 'from pass')
        pattern = re.compile(r'^(?=^.{6,32}$)(?=.*\d)(?=.*[0-9])(?=.*[A-Z])(?=.*[a-z]).*$')
        if re.match(pattern, password):
            return password
        else:
            raise ValidationError(
                '''Пароль должен быть минимум из 6ти символов,
                содержать хотя бы  одну цифру
                и хотя бы по одной букве в каждом регистре в латинице''')
