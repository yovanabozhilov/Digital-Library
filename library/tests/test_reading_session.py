from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from library.models import Book, ReadingSession
from datetime import timedelta
from django.utils import timezone
import re


def extract_minutes(text):
    if isinstance(text, (int, float)):
        return int(text)

    s = str(text)

    hours_match = re.search(r'(\d+)\s*час', s)
    mins_match  = re.search(r'(\d+)\s*минут', s)

    hours = int(hours_match.group(1)) if hours_match else 0
    mins  = int(mins_match.group(1)) if mins_match else 0
    return hours * 60 + mins


class ReadingSessionTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='reader', password='pass1234', email='r@r.r')
        self.book = Book.objects.create(title="Test Book", author="Author", added_by=self.user)

    def test_reading_session_duration_auto_computed(self):
        start = timezone.now() - timedelta(minutes=30)
        end = timezone.now()
        session = ReadingSession.objects.create(
            user=self.user,
            book=self.book,
            start_time=start,
            end_time=end,
            pages_read=10
        )
        self.assertAlmostEqual(session.duration_minutes, 30, delta=1)

    def test_profile_statistics_today_week_month(self):
        now = timezone.now()

        ReadingSession.objects.create(
            user=self.user, book=self.book,
            start_time=now - timedelta(minutes=30),
            end_time=now,
            pages_read=10
        )
        ReadingSession.objects.create(
            user=self.user, book=self.book,
            start_time=now - timedelta(days=5, minutes=30),
            end_time=now - timedelta(days=5),
            pages_read=12
        )
        ReadingSession.objects.create(
            user=self.user, book=self.book,
            start_time=now - timedelta(days=40, minutes=30),
            end_time=now - timedelta(days=40),
            pages_read=8
        )

        self.client.login(username='reader', password='pass1234')
        resp = self.client.get(reverse('profile'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('stats', resp.context)

        stats = resp.context['stats']
        self.assertIn('today_minutes', stats)
        self.assertIn('week_minutes', stats)
        self.assertIn('month_minutes', stats)

        today_m  = extract_minutes(stats['today_minutes'])
        week_m   = extract_minutes(stats['week_minutes'])
        month_m  = extract_minutes(stats['month_minutes'])

        self.assertAlmostEqual(today_m, 30, delta=1)   
        self.assertAlmostEqual(week_m, 60, delta=2)    
        self.assertAlmostEqual(month_m, 60, delta=2)   

        self.assertContains(resp, 'Статистика за четене')

    def test_main_page_today_stats_minutes_and_pages(self):
        now = timezone.now()
        ReadingSession.objects.create(
            user=self.user, book=self.book,
            start_time=now - timedelta(minutes=20),
            end_time=now - timedelta(minutes=10),
            pages_read=5
        )
        ReadingSession.objects.create(
            user=self.user, book=self.book,
            start_time=now - timedelta(minutes=9),
            end_time=now - timedelta(minutes=1),
            pages_read=7
        )

        self.client.login(username='reader', password='pass1234')
        resp = self.client.get(reverse('main'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('stats', resp.context)
        stats = resp.context['stats']

        self.assertIn('today_minutes', stats)
        self.assertIn('today_pages', stats)

        self.assertGreaterEqual(int(stats['today_minutes']), 17)
        self.assertLessEqual(int(stats['today_minutes']), 19)
        self.assertEqual(int(stats['today_pages']), 12)
