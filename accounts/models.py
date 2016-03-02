from PIL import Image, ImageFont, ImageDraw
from django.db.models import F
from django.utils import timezone
from django.contrib.auth.models import User
from django.db import models
from forum.settings import MEDIA_ROOT


class UserDetails(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(
        upload_to='%s/user_pics' % (MEDIA_ROOT, ),
        height_field=100,
        width_field=100,
        blank=True
    )

    @property
    def get_post_frequency(self):
        posts = self.user.message_set.count()
        date_joined = self.user.date_joined
        delta = (timezone.now() - date_joined).days

        if not posts:
            return 'Нет сообщений'

        elif not delta:
            return '%s сообщений за день' % (posts,)

        else:
            frequency = round(posts/delta, 1)
            return '%s сообщений в день' % (frequency,)

    def __str__(self):
        return 'user: %s additional info' % (self.user.username,)


class FilterNewManager(models.Manager):
    use_for_related_fields = True

    def get_unread(self):
        return super(FilterNewManager, self).get_queryset().filter(read=False)


class UserMessages(models.Model):
    receiver = models.ForeignKey(User)
    sender = models.ForeignKey(User, related_name='sender')
    title = models.CharField(max_length=150)
    message = models.TextField()
    read = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    objects = FilterNewManager()

    class Meta:
        ordering = ['-date']
