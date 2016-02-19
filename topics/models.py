from django.db import models
from django.contrib.auth.models import User

from section.models import Section


TOPIC_STATE = (
    ('C', 'Closed'),
    ('O', 'Open'),
    ('S', 'Closed by section')
)


class Moder(models.Model):
    moder = models.ForeignKey(User)

    class Meta:
        verbose_name_plural = 'Модераторы'


class Topic(models.Model):
    name = models.CharField(verbose_name='Тема', max_length=1000, unique_for_date='date')
    date = models.DateField(auto_now_add=True)
    state = models.CharField(max_length=1, choices=TOPIC_STATE, default='O')
    author = models.ForeignKey(User)
    moder = models.ForeignKey(Moder)
    section = models.ForeignKey(Section)

    class Meta:
        verbose_name_plural = 'Темы'

    def topic_icon(self):
        if self.state == 'O':
            return 'fa fa-comment-o fa-3x'
        else:
            return 'fa fa-lock fa-3x'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return "/%s/%s" % (self.section.slug ,self.pk)


class Message(models.Model):
    author = models.ForeignKey(User, verbose_name='Автор')
    topic = models.ForeignKey(Topic, verbose_name='Тема')
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст сообщения')
    rate = models.IntegerField('Рейтинг', default=0)

    def colorize(self):
        code = '*code*'
        return self.text.split(code) if self.text.count(code) == 2 else False

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = "Сообщение"
