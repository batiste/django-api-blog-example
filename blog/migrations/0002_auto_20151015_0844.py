# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Translation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language', models.CharField(default=b'en', max_length=2, choices=[(b'en', b'English'), (b'de', b'German'), (b'fr', b'French'), (b'it', b'Italian')])),
                ('slug', models.SlugField(default=uuid.uuid4, unique=True, max_length=300)),
                ('title', models.CharField(max_length=300)),
                ('content', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='Post',
            new_name='post',
        ),
        migrations.RemoveField(
            model_name='post',
            name='content',
        ),
        migrations.RemoveField(
            model_name='post',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
        migrations.AddField(
            model_name='translation',
            name='post',
            field=models.ForeignKey(to='blog.Post'),
        ),
    ]
