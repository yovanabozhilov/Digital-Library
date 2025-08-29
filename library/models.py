from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=100, blank=True)
    mood = models.CharField(max_length=255, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    language = models.CharField(max_length=100, blank=True) 
    added_by = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=[('to_read', 'За четене'), ('reading', 'Чета'), ('read', 'Прочетена')],
        default='to_read'
    )
    current_page = models.PositiveIntegerField(default=0)
    total_pages = models.PositiveIntegerField(default=0)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    description = models.TextField(blank=True)
    pdf_file = models.FileField(upload_to="ebooks/", blank=True, null=True)

    def __str__(self):
        return self.title

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return f"{self.user.username} – {self.book.title} ({self.rating})"

class JournalEntry(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.CharField(max_length=255, blank=True, null=True)
    page_end = models.PositiveIntegerField(blank=True, null=True)
    content = models.TextField(help_text="Write your notes, quotes, impressions, or anything else here.")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        page_info = f"p.{self.page}" if self.page else "no page"
        return f"Entry for {self.book.title} – {page_info}"

class SavedQuote(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quote_text = models.TextField()
    page = models.PositiveIntegerField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'"{self.quote_text[:30]}..." (p.{self.page})'

class EbookFile(models.Model):
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name='ebookfile')

    file = models.FileField(upload_to='ebooks/')
    last_page_read = models.TextField(default="", blank=True)

    def __str__(self):
        return f"Ebook for {self.book.title}"

class MyBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Chapter(models.Model):
    mybook = models.ForeignKey('MyBook', on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=255)
    content = models.TextField()  

    def __str__(self):
        return self.title

class WordLookup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    word = models.CharField(max_length=100)
    definition = models.TextField()

    class Meta:
        unique_together = ('user', 'word')  

    def __str__(self):
        return self.word

class ReadingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    duration_minutes = models.IntegerField(default=0)
    pages_read = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        self.duration_minutes = int((self.end_time - self.start_time).total_seconds() / 60)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} – {self.book.title} ({self.start_time.strftime('%Y-%m-%d')})"



