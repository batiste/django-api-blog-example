from django.db import models
from django.contrib.auth.models import User
import uuid

LANGS = (
    ('en', 'English'),
    ('de', 'German'),
    ('fr', 'French'),
    ('it', 'Italian'),
)


class Post(models.Model):

    #title = models.CharField(max_length=300)
    #slug = models.SlugField(max_length=300, unique=True, default=uuid.uuid4)
    author = models.ForeignKey(User)
    #content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __unicode__(self):
        trans = Translation.objects.filter(language='en', post=self)
        if len(trans):
            return trans[0].title
        return 'Unamed post from ' + self.author.username

    def title(self):
        trans = Translation.objects.filter(language='en', post=self)
        if len(trans):
            return trans[0].title
        return ''

    def slug(self):
        trans = Translation.objects.filter(language='en', post=self)
        if len(trans):
            return trans[0].slug
        return ''

    def content(self):
        trans = Translation.objects.filter(language='en', post=self)
        if len(trans):
            return trans[0].content
        return ''

    def url(self):
        return 

class Translation(models.Model):

    post = models.ForeignKey(Post)
    language = models.CharField(max_length=2, choices=LANGS, default='en')

    slug = models.SlugField(max_length=300, unique=True, default=uuid.uuid4)

    title = models.CharField(max_length=300)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):

    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)