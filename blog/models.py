from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):

    title = models.CharField(max_length=300)
    author = models.ForeignKey(User)
    content = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)