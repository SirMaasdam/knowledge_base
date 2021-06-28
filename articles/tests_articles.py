from django.test import TestCase, Client
from articles.models import Article
from django.contrib.auth import get_user_model

User = get_user_model()


class CreateContentTestCase(TestCase):
    def test_article_view(self):
        user = User.objects.create(username='TestUser1',
                                   password='password')
        article1 = Article.objects.create(id=1,
                                          user=user,
                                          title='Test Article',
                                          draft=False)
        datetime = article1.created
        client = Client()

        response = client.get('/articles/')
        self.assertEqual(response.status_code, 200)

        response = client.get('/articles/',
                              data={"year": datetime.year,
                                    "month": datetime.month,
                                    "day": datetime.day,
                                    "slug": article1.slug})
        self.assertEqual(response.status_code, 200)

