from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from library.models import MyBook, Chapter

class MyBookTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='creator', password='pass1234')
        self.client.login(username='creator', password='pass1234')
        self.mybook = MyBook.objects.create(user=self.user, title="My Novel")

    def test_create_mybook(self):
        response = self.client.post(reverse('create_mybook'), {'title': 'My New Book'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(MyBook.objects.filter(title='My New Book', user=self.user).exists())

    def test_view_mybook(self):
        url = reverse('view_mybook', args=[self.mybook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.mybook.title)

    def test_add_chapter(self):
        url = reverse('add_chapter', args=[self.mybook.id])
        response = self.client.post(url, {'title': 'Chapter 1', 'content': 'Content goes here'}, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Chapter.objects.filter(mybook=self.mybook, title='Chapter 1').exists())

    def test_edit_chapter(self):
        chapter = Chapter.objects.create(mybook=self.mybook, title='Old Title', content='Old content')
        url = reverse('edit_chapter', args=[self.mybook.id, chapter.id])
        response = self.client.post(url, {
            'title': 'New Title',
            'content': 'Updated content'
        }, follow=True)
        chapter.refresh_from_db()
        self.assertEqual(chapter.title, 'New Title')
        self.assertEqual(chapter.content, 'Updated content')

    def test_export_mybook_docx(self):
        url = reverse('export_mybook_docx', args=[self.mybook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document')

    def test_export_mybook_pdf(self):
        url = reverse('export_mybook_pdf', args=[self.mybook.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'application/pdf')