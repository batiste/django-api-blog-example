from django.http import Http404
from django.shortcuts import render_to_response
from blog.models import Post

def index(request):
    posts = Post.objects.all()[:5]
    return render_to_response('index.html', {'posts': posts})