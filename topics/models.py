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

    def __str__(self):
        return self.moder.username


class Topic(models.Model):
    name = models.CharField(verbose_name='Тема', max_length=1000, unique_for_date='date')
    short_description = models.CharField(verbose_name='Карткое описание',
                                         max_length=150,
                                         blank=True,
                                         null=True)
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

    def get_absolute_url(self):
        return "/%s/%s" % (self.section.slug ,self.pk)

    def __str__(self):
        return self.name


class Message(models.Model):
    title = models.CharField(max_length=150, blank=True)
    author = models.ForeignKey(User, verbose_name='Автор')
    topic = models.ForeignKey(Topic, verbose_name='Тема')
    date = models.DateField('Дата', auto_now_add=True)
    text = models.TextField('Текст сообщения')
    rate = models.IntegerField('Рейтинг', default=0)

    class Meta:
        verbose_name_plural = 'Сообщения'
        verbose_name = "Сообщение"

    def colorize(self):
        code = '*code*'
        return self.text.split(code) if self.text.count(code) == 2 else False

    def __str__(self):
        return self.text

