from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models


class UserDetails(models.Model):
    user = models.OneToOneField(User)
    # avatar = models.ImageField(upload_to='')

    def __str__(self):
        return 'user: %s additional info' % (self.user.username,)

    @property
    def users_post(self):
        return self.user.message_set.all()

    @property
    def get_post_frequency(self):
        posts = self.user.message_set.count()
        date_joined = self.user.date_joined
        delta = timezone.now() - date_joined
        frequency = round(posts/delta.days, 1)

        return '%s сообщений в день' % (frequency,)


class UserMessages(models.Model):
    receiver = models.OneToOneField(User, related_name='receiver')
    sender = models.OneToOneField(User, related_name='sender')
    title = models.CharField(max_length=150)
    message = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
