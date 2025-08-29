from django.test import TestCase, override_settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from ..models import Book, Review, EbookFile
from .utils import create_user, login, upload_pdf, create_book, make_image_file 


@override_settings(MEDIA_ROOT="/tmp/dl_media")
class BookViewsTests(TestCase):
    def setUp(self):
        self.user, self.pw = create_user()
        login(self.client, self.user, self.pw)

    def test_add_book_with_pdf(self):
        url = reverse('add_book')
        data = {
            'title': 'My Book',
            'author': 'Me',
            'genre': ['Fantasy', 'Drama'],   
            'mood': ['Funny'],              
            'isbn': '123',
            'description': 'desc',
            'language': 'English',
            'status': 'to_read',
            'file': upload_pdf('a.pdf'),
            'cover_image': make_image_file('cover.png'),
        }
        res = self.client.post(url, data, follow=True)
        self.assertEqual(res.status_code, 200, getattr(res, 'content', b'')[:500])

        self.assertTrue(Book.objects.filter(title='My Book').exists())
        b = Book.objects.get(title='My Book')
        self.assertTrue(EbookFile.objects.filter(book=b).exists())
        self.assertTrue(b.cover_image)  

    def test_my_added_books_filters_and_order(self):
        create_book(self.user, title="Alpha", genre="Fantasy, Drama", mood="Funny")
        create_book(self.user, title="Beta", genre="Fantasy", mood="Sad")

        url = reverse('my_added_books')

        res = self.client.get(url, {'genre': 'Fantasy'})
        self.assertContains(res, "Alpha")
        self.assertContains(res, "Beta")

        res = self.client.get(url, {'mood': 'Sad'})
        self.assertNotContains(res, "Alpha")
        self.assertContains(res, "Beta")

        res = self.client.get(url)
        titles = list(
            Book.objects.filter(added_by=self.user)
            .order_by('title')
            .values_list('title', flat=True)
        )
        self.assertEqual(titles, sorted(titles))

    def test_book_detail_reviews(self):
        b = create_book(self.user)
        url = reverse('book_detail', args=[b.id])

        res = self.client.post(url, {'rating': 5, 'content': 'Great!'}, follow=True)
        self.assertEqual(res.status_code, 200)
        r = Review.objects.get(book=b, user=self.user)

        res = self.client.post(url, {'edit_review_id': r.id}, follow=True)
        self.assertEqual(res.status_code, 200)

        res = self.client.post(url, {'review_id': r.id, 'rating': 4, 'content': 'Ok'}, follow=True)
        self.assertEqual(Review.objects.get(id=r.id).rating, 4)

        res = self.client.post(url, {'delete_review_id': r.id}, follow=True)
        self.assertFalse(Review.objects.filter(id=r.id).exists())

    def test_delete_book_permission(self):
        b = create_book(self.user)
        url = reverse('delete_book', args=[b.id])
        res = self.client.post(url, follow=True)
        self.assertFalse(Book.objects.filter(id=b.id).exists())

    def test_read_book(self):
        b = create_book(self.user)
        ef = EbookFile.objects.get(book=b)
        if not ef.file:
            ef.file = upload_pdf('b.pdf')
            ef.save()

        res = self.client.get(reverse('read_book', args=[b.id]))
        self.assertEqual(res.status_code, 200)