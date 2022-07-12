import html
from django.urls import resolve
from django.test import TestCase
from .views import home_page, article_page
from .models import Article
from django.http import HttpRequest
from django.urls import reverse
from datetime import datetime
import pytz
class ArticlePageTest(TestCase):

    def test_article_page_displays_correct_article(self):
        Article.objects.create(
            title='title 1',
            summary='summary 1',
            full_text='full_text 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-1',
        )

        request = HttpRequest()
        response = article_page(request, 'slug-1')
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('full_text 1', html)
        self.assertNotIn('summary 1', html)

class HomePageTest(TestCase):

    def test_home_page_displays_articles(self):
        Article.objects.create(
            title='title 1',
            summary='summary 1',
            full_text='full_text 1',
            categery='categery-1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-1',
        )
        Article.objects.create(
            title='title 2',
            summary='summary 2',
            full_text='full_text 2',
            categery='categery-1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-2',
        )

        request = HttpRequest()
        response = home_page(request)
        html = response.content.decode('utf8')

        self.assertIn('title 1', html)
        self.assertIn('/blog/slug-1', html)
       # self.assertNotIn('summary 1', html)
       # self.assertIn('full_text 1', html)

        self.assertIn('title 2', html)
        self.assertIn('/blog/slug-2', html)
       # self.assertNotIn('summary 2', html)
       # self.assertIn('full_text 2', html)

    def test_home_page_returns_correct_html(self):
        url = reverse('home_page')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'home_page.html')


class ArticleModelTest(TestCase):
    def test_article_model_save_and_retrieve(self):
        # создай пост 1
        # сохрани пост 1
        article1 = Article(
            title='article 1',
            full_text='full_text 1',
            summary='summary 1',
            categery='categery 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-1',
        )
        article1.save()
        # создай пост 2
        # сохрани пост 2
        article2 = Article(
            title='article 2',
            full_text='full_text 2',
            summary='summary 2',
            categery='categery 2',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-2',
        )
        article2.save()

        # загрузи из базы все посты
        all_articles = Article.objects.all()

        # проверь: постов 2
        self.assertEqual(len(all_articles), 2)
        # проверь: 1 загружен из базы пост == пост 1
        self.assertEqual(
            all_articles[0].title,
            article1.title
        )
        self.assertEqual(
            all_articles[0].slug,
            article1.slug
        )
        # проверь: 2 загружен из базы пост == пост 2
        self.assertEqual(
            all_articles[1].title,
            article2.title
        )
        self.assertEqual(
            all_articles[1].slug,
            article2.slug
        )

