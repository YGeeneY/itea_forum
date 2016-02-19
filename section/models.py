import uuid

from django.db.models.signals import post_save
from unidecode import unidecode

from django.db import models
from django.utils.text import slugify


class Section(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(blank=True)
    is_open = models.BooleanField(default=True)

    def last_five(self):
        return self.topic_set.all()[:5]

    def make_slug(self):
        unique = str(uuid.uuid4())[:5]
        ascii_name = unidecode(self.name)[:45]
        slug = slugify(ascii_name) + unique
        try:
            Section.objects.get(slug=slug)
            self.make_slug()
        except Section.DoesNotExist:
            return slug

    def save(self, *args, **kwargs):
        self.slug = self.make_slug()
        super(Section, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


def close_section_topics(instance, **kwargs):
    if instance.is_open:
        for topic in instance.topic_set.filter(state='S'):
            topic.state = 'O'   # close it by section is_open state
            topic.save()
    else:
        for topic in instance.topic_set.filter(state='O'):
            topic.state = 'S'
            topic.save()

post_save.connect(close_section_topics, sender=Section)
