from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
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
        trans = self.translation_for_lang('en')
        if trans:
            return trans.title
        return 'Unamed post from ' + self.author.username

    def translation_for_lang(self, lang):
        trans = Translation.objects.filter(language=lang, post=self)
        if len(trans):
            return trans[0]
        trans = Translation.objects.filter(post=self)
        return trans[0]

    def translations(self):
        return Translation.objects.filter(post=self)

    def get_absolute_url(self):
        trans = self.translation_for_lang('en')
        if not trans:
            return '/'
        return trans.get_absolute_url()


class Translation(models.Model):

    post = models.ForeignKey(Post)
    language = models.CharField(max_length=2, choices=LANGS, default='en')

    slug = models.SlugField(max_length=300, unique=True, default=uuid.uuid4)

    title = models.CharField(max_length=300)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        year = self.post.created.year
        month = self.post.created.month
        day = self.post.created.day
        return reverse('post_details', kwargs={
            'lang':self.language, 
            'year':year,
            'month':month, 
            'day':day, 
            'slug':self.slug})

    def __unicode__(self):
        return self.slug


class Comment(models.Model):

    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)