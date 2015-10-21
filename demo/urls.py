"""demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from blog.serializers import router
from blog import views

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = 'Local.ch Blog'

urlpatterns = [
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(router.urls)),
    url(r'^$', views.index),
    url(r'^(?P<lang>[a-z]{2})/$', views.index),
    # en/2015/10/20/our-worry-free-package/
    url(r'^(?P<lang>[a-z]{2})/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/(?P<day>[0-9]{1,2})/(?P<slug>\w[\w\-]*\w)/$', views.details, name="post_details"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
