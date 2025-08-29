import json
from datetime import timedelta
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone
from ..models import ReadingSession, EbookFile
from .utils import create_user, login, create_book

class ReadingEndpointsTests(TestCase):
    def setUp(self):
        self.user, self.pw = create_user()
        login(self.client, self.user, self.pw)
        self.book = create_book(self.user)

    def test_save_last_page_updates_ebook(self):
        url = reverse('save_last_page', args=[self.book.id])
        payload = {'page': 42}
        res = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.book.refresh_from_db()
        self.assertEqual(self.book.ebookfile.last_page_read, "42")
