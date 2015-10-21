import requests
import datetime
from bs4 import BeautifulSoup
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
import django
django.setup()
from blog.models import Post, Translation
from django.contrib.auth.models import User
import requests
import shutil


r = requests.get('http://blog.local.ch/en/category/news/')

def byClass(soup, type, cls):
    return byAttr(soup, type, 'class', cls)

def byAttr(soup, type, attrname, value):
    result = []
    for el in soup.find_all(type):
        if el.has_attr(attrname) and value in el[attrname]:
            result.append(el)
    return result

articles_to_visit = []

def extract_articles(soup):
    for title in byClass(soup, 'h2', 'memonic_title'):
        url = title.find('a')['href']
        if url not in articles_to_visit:
          articles_to_visit.append(url)

def save_image(url, path):
    if os.path.isfile(path):
        return
    r = requests.get(url, stream=True)
    if r.status_code == 200:
        with open(path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)

def extract_images(soup):
    images = soup.find_all('img')
    for image in images:
        url = image['src']
        if url.startswith('data:'):
            continue
        filename = url.split('/')[-1:][0]
        save_image(url, 'blog/media/images/' + filename)
        image['src'] = '/media/images/' + filename


def extract_article_data(url):
    print url
    r = requests.get(url)
    if r.status_code != 200:
        print '-----------------------'
        print r.status_code
        return

    soup = BeautifulSoup(r.text, 'html.parser')
    title = byClass(soup, 'h1', 'memonic_title')[0]
    title = title.get_text()

    lang_urls = {}
    el = byClass(soup, 'ul', 'langnav')[0]
    for link in el.find_all('a'):
        lang_urls[link.get_text().lower()] = link['href']

    content_node = byClass(soup, 'div', 'content')[0]
    for link in content_node.find_all('a'):
        if link.has_key('href'):
            if link['href'].startswith('http://static.blog.local.ch/'):
                filename = link['href'].split('/')[-1:][0]
                link['href'] = '/media/images/' + filename
            if link['href'].startswith('http://blog.local.ch/'):
                link['href'] = link['href'].replace('http://blog.local.ch/', '/')

    extract_images(content_node)
    content = ""
    for child in content_node.children:
        content += unicode(child)

    data = url.split('/')
    date = datetime.date(int(data[4]), int(data[5]), int(data[6]))
    slug = data[7]

    author = byAttr(soup, 'a', 'rel', 'author')

    if len(author) and len(author[0].getText()):
        author_name = author[0].getText()
        first_name = author_name.split(' ')[0]
        if len(author_name.split(' ')) > 1:
            last_name = author_name.split(' ')[1]
        else:
            last_name = 'Unknown'
    else:
        author_name = 'Unknown'
        first_name = 'Unknown'
        last_name = 'Unknown'

    return locals()


def process_article(url):
    data = extract_article_data(url)
    if not data:
        return

    first_name = data['first_name']
    last_name = data['last_name']
    date = data['date']
    slug = data['slug']
    content = data['content']
    title = data['title']

    user, created = User.objects.get_or_create(username=first_name, first_name=first_name, last_name=last_name)
    Post._meta.get_field_by_name('created')[0].auto_now_add = False

    try:
        trans = Translation.objects.get(slug=slug)
        trans.content = content
        trans.save()
        post = trans.post
    except Translation.DoesNotExist:
        post = Post(created=date, updated=date, author=user)
        post.created = date
        post.update = date
        post.save()
        trans = Translation(post=post, content=content, title=title, slug=slug, language='en')
        trans.save()

    for lang in ['fr', 'de', 'it']:
        url = data['lang_urls'][lang]
        try:
            trans = Translation.objects.get(post=post, language=lang)
            if(len(url) > 30):
                data = extract_article_data(url)
                if(data):
                    trans.content = data['content']
                    trans.save()
        except Translation.DoesNotExist:
            if(len(url) > 30):
                data = extract_article_data(url)
                trans = Translation(post=post, content=data['content'], title=data['title'], slug=data['slug'], language=lang)
                trans.save()


index = 1
while True:
    print('Page %d' % index)
    r = requests.get('http://blog.local.ch/en/category/news/page/%d/' % index)
    if r.status_code != 200 or index > 100:
        print r.status_code
        break

    soup = BeautifulSoup(r.text, 'html.parser')
    extract_articles(soup)

    index = index + 1
    #break

index = 0
for url in articles_to_visit:
    process_article(url)

