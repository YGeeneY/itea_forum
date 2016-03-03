from django import forms
from topics.models import Message


class MessageModelForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text', )
        labels = {
            'text': 'Текст сообщения:'
        }
