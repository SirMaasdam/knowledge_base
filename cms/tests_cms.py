import io
import sys

from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile, InMemoryUploadedFile
from django.utils.datastructures import MultiValueDict

from articles.models import Article, Content, Image, Title, Text
from cms.create_content_services import manage_text_content, manage_image_content

User = get_user_model()


class CreateContentTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='test_user',
                                       password='password')
        cls.article = Article.objects.create(user=cls.user,
                                             title='Тестовая статья')
        file1 = SimpleUploadedFile('test_image1.jpg',
                                   content=b'',
                                   content_type='image/jpg')
        file2 = SimpleUploadedFile('test_image2.jpg',
                                   content=b'',
                                   content_type='image/jpg')
        cls.image1 = Image.objects.create(owner=cls.user,
                                          file=file1)
        cls.title1 = Title.objects.create(owner=cls.user,
                                          content="Это первый тестовый заголовок")
        cls.text = Text.objects.create(owner=cls.user,
                                       content="Это тестовый текст")
        cls.title2 = Title.objects.create(owner=cls.user,
                                          content="Это второй тестовый заголовок")
        cls.image2 = Image.objects.create(owner=cls.user,
                                          file=file2)
        cls.content_image1 = Content.objects.create(article=cls.article,
                                                    item=cls.image1)
        cls.content_title1 = Content.objects.create(article=cls.article,
                                                    item=cls.title1)
        cls.content_text = Content.objects.create(article=cls.article,
                                                  item=cls.text)
        cls.content_title2 = Content.objects.create(article=cls.article,
                                                    item=cls.title2)
        cls.content_image2 = Content.objects.create(article=cls.article,
                                                    item=cls.image2)

    def test_a_manage_text_content(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        request_data_for_text = {
            "1":
                {
                    "article_id": 1,
                    "content": "Это первый тестовый заголовок",
                    "item_type": "title",
                    "order": 1,
                    "item_id": 1,
                    "content_id": 2,
                    "delete": False,
                    "old_item": True
                },
            "2":
                {
                    "article_id": 1,
                    "content": "Это тестовый текст",
                    "item_type": "text",
                    "item_id": 1,
                    "content_id": 3,
                    "delete": True,
                    "old_item": True
                },
            "3":
                {
                    "article_id": 1,
                    "content": "Это измененный второй тестовый заголовок",
                    "item_type": "title",
                    "order": 2,
                    "item_id": 2,
                    "content_id": 4,
                    "delete": False,
                    "old_item": True
                },
            "4":
                {
                    "article_id": 1,
                    "content": "Это новый тестовый заголовок",
                    "item_type": "title",
                    "order": 3,
                    "item_id": None,
                    "content_id": None,
                    "delete": False,
                    "old_item": False
                }
        }

        manage_text_content(request_data_for_text, request.user, self.article)

        self.assertEqual(self.article.contents.count(), 5)

        self.assertIn(self.content_title1, self.article.contents.all())
        self.assertEqual(self.content_title1.order, 1)
        self.assertEqual(self.content_title1.item.content, "Это первый тестовый заголовок")
        self.assertEqual(self.content_title1.item.owner, self.user)

        self.assertNotIn(self.content_text, self.article.contents.all())

        title2 = self.article.contents.all()[2]
        self.assertIn(title2, self.article.contents.all())
        self.assertEqual(title2.order, 2)
        self.assertEqual(title2.item.content, "Это измененный второй тестовый заголовок")
        self.assertEqual(title2.item.owner, self.user)

        title3 = Content.objects.get(pk=6)
        self.assertIn(title3, self.article.contents.all())
        self.assertEqual(title3.order, 3)
        self.assertEqual(title3.item.content, "Это новый тестовый заголовок")
        self.assertEqual(title3.item.owner, self.user)

    def test_b_manage_image_content(self):
        factory = RequestFactory()
        request = factory.get('')
        request.user = self.user
        request_data_for_file = {
            '0': ['1', 'delete', '1'],
            '5': ['1', '4', '5'],
            '6': ['1', '5', 'adding']
        }

        img_io = io.BytesIO()
        file = InMemoryUploadedFile(img_io,
                                    'ImageField',
                                    'test_image3.jpg',
                                    'JPEG',
                                    sys.getsizeof(img_io), None)
        files = MultiValueDict({'6': [file]})

        manage_image_content(request_data_for_file, request.user, files, None)

        self.assertEqual(self.article.contents.count(), 5)

        self.assertNotIn(self.content_image1, self.article.contents.all())

        self.assertIn(self.content_image2, self.article.contents.all())
        self.assertEqual(self.content_image2.order, 4)
        self.assertEqual(self.content_image2.item.owner, self.user)

        image3 = Content.objects.get(id=7)
        self.assertIn(image3, self.article.contents.all())
        self.assertEqual(image3.order, 5)
        self.assertEqual(image3.item.owner, self.user)

