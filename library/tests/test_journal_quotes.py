from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
import json

from library.models import Book, SavedQuote, JournalEntry

class JournalAndQuoteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='reader', password='pass1234', email='r@r.r')
        self.client.login(username='reader', password='pass1234')
        self.book = Book.objects.create(title="Quote Book", author="Author", added_by=self.user)

    def test_save_highlighted_quote_pdf(self):
        url = reverse('save_quote')
        payload = {
            'book_id': self.book.id,
            'text': 'To be or not to be',
            'page': 5
        }
        res = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(res.json().get('status'), 'ok')
        self.assertTrue(SavedQuote.objects.filter(book=self.book, user=self.user, page=5, quote_text__startswith='To be').exists())

    def test_delete_quote(self):
        q = SavedQuote.objects.create(book=self.book, user=self.user, quote_text='Line', page=2)
        url = reverse('delete_quote')
        res = self.client.post(url, data=json.dumps({'id': q.id}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get('status'), 'ok')
        self.assertFalse(SavedQuote.objects.filter(id=q.id).exists())

    def test_save_note(self):
        url = reverse('save_note')
        payload = {
            'book_id': self.book.id,
            'content': 'My reflection on the chapter.',
            'page': '12'   
        }
        res = self.client.post(url, data=json.dumps(payload), content_type='application/json')
        self.assertEqual(res.status_code, 200, res.content)
        self.assertEqual(res.json().get('status'), 'ok')
        self.assertTrue(JournalEntry.objects.filter(book=self.book, user=self.user, page='12', content__startswith='My reflection').exists())

    def test_delete_note(self):
        n = JournalEntry.objects.create(book=self.book, user=self.user, content='Note', page='7')
        url = reverse('delete_note')
        res = self.client.post(url, data=json.dumps({'id': n.id}), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json().get('status'), 'ok')
        self.assertFalse(JournalEntry.objects.filter(id=n.id).exists())

    def test_read_book_context_includes_quotes_and_notes(self):
        SavedQuote.objects.create(book=self.book, user=self.user, quote_text='Important line', page=3)
        JournalEntry.objects.create(book=self.book, user=self.user, content='Note text', page='3')

        res = self.client.get(reverse('read_book', args=[self.book.id]))
        self.assertEqual(res.status_code, 200)
        self.assertIn('quotes', res.context)
        self.assertIn('notes', res.context)
        self.assertEqual(res.context['book'].id, self.book.id)
        self.assertEqual(res.context['quotes'].count(), 1)
        self.assertEqual(res.context['notes'].count(), 1)
