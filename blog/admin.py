from django.contrib import admin
from blog.models import Post
from django import forms
from ckeditor.widgets import CKEditorWidget

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Post
        fields = ('title', 'author', 'content')

class PostAdmin(admin.ModelAdmin):
    
    form = PostAdminForm

    list_display = ('title', 'author', 'created', 'updated')
    list_filter = ('author', 'created', 'updated')
    search_fields = ('title', 'author__username', 'content')

admin.site.register(Post, PostAdmin)

