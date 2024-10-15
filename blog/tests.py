from django.test import TestCase
from django.urls import reverse

from user.models import Writer
from blog.models import Article


class ArticleOpsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.writer = Writer.objects.create(
            username="obiwankena",
            is_editor=False,
        )
        cls.writer.set_password("123")
        cls.writer.save()

        cls.editor = Writer.objects.create(
            username="editor_user",
            is_editor=True,
        )
        cls.editor.set_password("123")
        cls.editor.save()

    @classmethod
    def tearDownClass(cls): ...

    def test_create_article_view(self):
        self.client.login(username="obiwankena", password="123")
        client = self.client
        data = {
            "title": "Test Title",
            "content": "Dummy data",
        }
        response = client.post(
            path=reverse("create-article"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        article = Article.objects.filter(title="Test Title").first()
        self.assertIsNone(article)
        self.client.logout()

    def test_is_writer_can_see_approval_page(self):
        self.client.login(username="obiwankena", password="123")
        response = self.client.get(reverse("article-approval"))
        self.assertEqual(response.url, "/")
        self.client.logout()

    def test_is_editor_can_see_approval_page(self):
        self.client.login(username="editor_user", password="123")

        response = self.client.get(reverse("article-approval"))
        self.assertTrue("Article Approval Page" in response.content.decode("utf-8"))
        self.client.logout()

    def test_approve_and_article_as_editor(self):
        self.client.login(username="editor_user", password="123")
        article = Article.objects.create(
            title="Test title", content="Test Dummy data", written_by=self.writer
        )
        approve_data = {
            "approve": "approve",
        }
        self.assertEqual(article.status, Article.DRAFT)
        self.client.post(
            path=reverse("article-approval", kwargs={"pk": article.pk}),
            data=approve_data,
        )
        article.refresh_from_db()
        self.assertEqual(article.status, Article.APPROVED)
