from unittest.mock import patch, MagicMock
from django.test import TestCase
from django.urls import reverse
from .utils import create_user, login
from ..models import WordLookup

class DictionaryTests(TestCase):
    def setUp(self):
        self.user, self.pw = create_user()
        login(self.client, self.user, self.pw)

    @patch('library.views.requests.get')
    @patch('library.views.Translator')
    def test_translate_and_define_en_word(self, mock_translator_cls, mock_requests_get):
        mock_translator = MagicMock()
        mock_translator.translate.side_effect = lambda text, src, dest: MagicMock(text="котка")
        mock_translator_cls.return_value = mock_translator

        mock_dict_resp = MagicMock()
        mock_dict_resp.status_code = 200
        mock_dict_resp.json.return_value = [{
            "meanings": [
                {"partOfSpeech": "noun", "definitions": [{"definition": "a small domesticated carnivorous mammal"}]},
                {"partOfSpeech": "verb", "definitions": [{"definition": "to raise the back"}]}
            ]
        }]
        mock_requests_get.return_value = mock_dict_resp

        res = self.client.get(reverse('translate_define'), {'word': 'cat'})
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(data['original'], 'cat')
        self.assertEqual(data['translated'], 'котка')
        self.assertIn('noun', data['definitions'])
        self.assertIn('verb', data['definitions'])

        self.assertTrue(WordLookup.objects.filter(user=self.user, word='cat').exists())

    @patch('library.views.Translator')
    def test_translate_define_no_word(self, _):
        res = self.client.get(reverse('translate_define'), {})
        self.assertEqual(res.status_code, 200)
        self.assertIn('error', res.json())
