from django.http import Http404
from django.shortcuts import render_to_response
from blog.models import Post, Translation, LANGS
from django.utils import translation
from django.core.paginator import Paginator

def index(request, lang=None):
    if lang:
        translation.activate(lang)
    language = lang or request.LANGUAGE_CODE
    page_number = request.GET.get('page', 1)
    paginator = Paginator(Post.objects.all(), 5)
    page = paginator.page(page_number)

    translations = []
    for post in page.object_list:
        trans = post.translation_for_lang(language)
        if trans:
            translations.append(post.translation_for_lang(language))
    return render_to_response('index.html', {
        'translations': translations, 
        'lang':request.LANGUAGE_CODE,
        'langs': LANGS,
        'page': page
    })

def details(request, lang, year, month, day, slug):
    trans = Translation.objects.filter(slug=slug, language=lang)
    translation.activate(lang)
    if len(trans) > 0:
        trans = trans[0]
    else:
        raise Http404("Post does not exist")
    print trans.post.translations()
    return render_to_response('details.html', {'translation': trans})