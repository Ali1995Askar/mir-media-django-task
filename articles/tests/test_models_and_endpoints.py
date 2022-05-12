from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Article

LIST_ARTICLES_URL = reverse('articles:articles-list')

USER_MODEL = get_user_model()


class TestArticleApp(TestCase):
    def setUp(self) -> None:
        self.user_payload = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'username': 'username',
            'password': 'TestPassword12345'

        }
        self.article_title = 'Test article title'
        self.article_content = 'Test article content bla bla bla bla >>>>!!!!'

        self.num_of_online_articles = 35
        self.num_of_offline_articles = 25

        self.user = USER_MODEL.objects.create_user(**self.user_payload)

    def test_create_article_with_correct_values(self):
        article = Article.objects.create(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        )
        self.assertTrue(article.status)
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.title, self.article_title)
        self.assertEqual(article.content, self.article_content)

        self.assertEqual(Article.objects.all().count(), 1)

    def test_bulk_create_articles_with_slugs_fields(self):
        online_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        ) for i in range(self.num_of_online_articles)]

        offline_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content,
            status=False
        ) for i in range(self.num_of_offline_articles)]

        Article.objects.bulk_create(online_articles)
        self.assertEqual(Article.objects.filter(status=True).count(), self.num_of_online_articles)

        Article.objects.bulk_create(offline_articles)
        self.assertEqual(Article.objects.filter(status=False).count(), self.num_of_offline_articles)

        self.assertEqual(Article.objects.all().count(), self.num_of_online_articles + self.num_of_offline_articles)

    def test_switch_article_status_method_and_property(self):
        article = Article.objects.create(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        )
        self.assertTrue(article.status)
        self.assertTrue(article.is_online)

        article.switch_status()
        article.refresh_from_db()

        self.assertFalse(article.status)
        self.assertFalse(article.is_online)

    def test_get_list_articles_only_5_endpoint_with_online_status_only(self):
        online_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        ) for i in range(self.num_of_online_articles)]

        offline_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content,
            status=False
        ) for i in range(self.num_of_offline_articles)]

        Article.objects.bulk_create(online_articles)
        Article.objects.bulk_create(offline_articles)
        response = self.client.get(LIST_ARTICLES_URL)
        objects = response.context.get('articles')
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(objects,
                                 Article.objects.filter(status=True).order_by('-pub_date')[:5])

        self.assertEqual(objects.count(), 5)

    def test_get_list_articles_pagination(self):
        online_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        ) for i in range(self.num_of_online_articles)]

        offline_articles = [Article(
            author=self.user,
            title=self.article_title,
            content=self.article_content,
            status=False
        ) for i in range(self.num_of_offline_articles)]

        Article.objects.bulk_create(online_articles)
        Article.objects.bulk_create(offline_articles)
        response = self.client.get(LIST_ARTICLES_URL)
        objects = response.context.get('articles')

        self.assertEqual(response.context['paginator'].num_pages, self.num_of_online_articles // 5)
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(objects, Article.objects.filter(status=True).order_by('-pub_date')[:5])
        self.assertEqual(objects.count(), 5)

    def test_get_article_details_endpoint(self):
        Article.objects.create(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        )

        active_article = Article.objects.create(
            author=self.user,
            title=self.article_title,
            content=self.article_content
        )

        un_active_article = Article.objects.create(
            author=self.user,
            title=self.article_title,
            content=self.article_content,
            status=False
        )

        details_active_article_url = reverse('articles:article-details', kwargs={
            'pk': active_article.pk,
            'slug': active_article.slug
        })

        details_un_active_article_url = reverse('articles:article-details', kwargs={
            'pk': un_active_article.pk,
            'slug': un_active_article.slug
        })

        ok_response = self.client.get(details_active_article_url)
        obj = ok_response.context.get('article')

        self.assertEqual(ok_response.status_code, 200)
        self.assertEqual(obj.pk, active_article.pk)
        self.assertEqual(obj.slug, active_article.slug)
        self.assertEqual(obj.author, active_article.author)
        self.assertEqual(obj.title, active_article.title)
        self.assertEqual(obj.content, active_article.content)

        not_found_response = self.client.get(details_un_active_article_url)
        self.assertEqual(not_found_response.status_code, 404)
