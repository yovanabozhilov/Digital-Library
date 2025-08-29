from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from .utils import create_user, login, create_book

class RecommendationsTests(TestCase):
    def setUp(self):
        self.user, self.pw = create_user()
        login(self.client, self.user, self.pw)
        b = create_book(self.user, title="Read One", author="Some Author", genre="Fantasy", mood="Funny")
        b.status = 'read'
        b.save()

    @patch('library.views.requests.get')  
    def test_external_recommendations_dedup_and_limit(self, mock_get):
        def mk_item(title, authors=None):
            return {
                'volumeInfo': {
                    'title': title,
                    'authors': authors or ['Anon'],
                    'description': 'lorem',
                    'imageLinks': {'thumbnail': 'http://thumb'},
                    'infoLink': 'http://info'
                }
            }
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {'items': [mk_item(f"Title {i}") for i in range(1, 8)]}
        mock_get.return_value = mock_resp

        res = self.client.get(reverse('main'))
        self.assertEqual(res.status_code, 200)
        self.assertIn('external_recommendations', res.context)
        self.assertGreaterEqual(len(res.context['external_recommendations']), 1)
        self.assertLessEqual(len(res.context['external_recommendations']), 10)
