from selenium import webdriver
from selenium.webdriver.common.by import By
from django.test import LiveServerTestCase
from blog23.models import Article
from datetime import datetime
import pytz
import os
import unittest
from selenium.webdriver.remote.webelement import WebElement


class BlogTests(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Chrome()
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server

        Article.objects.create(
            title='article 1',
            full_text='full_text 1',
            summary='summary 1',
            categery='categery 1',
            pubdate=datetime.utcnow().replace(tzinfo=pytz.utc),
            slug='slug-1',
        )

    def tearDown(self):
        self.browser.quit()

    def test_home_page_title(self):
        self.browser.get(self.live_server_url)
        self.assertIn('Сайт Валентина Казюля', self.browser.title)

    def test_home_page_header(self):
        self.browser.get(self.live_server_url)
        header = self.browser.find_element(By.TAG_NAME,'h1')
        self.assertIn('Валентин Казюль', header.text)

    def test_layout_and_styling(self):
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        header = self.browser.find_element(By.TAG_NAME,'h1')
        self.assertTrue(header.location['x'] > 10)

    def test_home_page_blog(self):
        self.browser.get(self.live_server_url)
        article_list = self.browser.find_element(By.CLASS_NAME, 'article-list')
        self.assertTrue(article_list)

    def test_home_page_articles_look_correct(self):
        # У каждой статьи есть заголовок и один абзац с текстом
        self.browser.get(self.live_server_url)
        article_title = self.browser.find_element(
            By.CLASS_NAME,
            'article-title')

        self.assertTrue(article_title)
        # self.assertTrue(article_text)




    def test_home_page_article_title_link_leads_to_article_page(self):
        self.browser.get(self.live_server_url)
        article_title = self.browser.find_element(By.CLASS_NAME,
            'article-title')
        article_title_text = article_title.text

        article_link = article_title.find_element(By.TAG_NAME, 'a')
        self.browser.get(article_link.get_attribute('href'))
        article_page_title = self.browser.find_element(By.CLASS_NAME,
            'article-title')

        self.assertEqual(article_title_text, article_page_title.text)

