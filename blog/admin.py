from django.contrib import admin
from blog.models import Post, Comment, Translation
from django import forms
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget

class TranslationAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Translation
        fields = ('language', 'title', 'slug', 'content')


class TranslationInline(admin.StackedInline):
    form = TranslationAdminForm
    model = Translation
    extra = 1
    max_num = 4

class PostAdmin(admin.ModelAdmin):

    inlines = [
        TranslationInline,
    ]

    list_display = ('__unicode__', 'author', 'created', 'updated')
    list_filter = ('author', 'created', 'updated')
    search_fields = ('author__username',)

admin.site.register(Post, PostAdmin)
admin.site.register(Comment)

