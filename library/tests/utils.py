from django.contrib.auth.models import User
from django.test import Client
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO
from library.models import Book, EbookFile

DEFAULT_PW = "testpass"

def create_user(username="testuser", password=DEFAULT_PW):
    user, _ = User.objects.get_or_create(username=username, defaults={"email": f"{username}@example.com"})
    user.set_password(password)
    user.save()
    return user, password  

def login(client: Client, user_or_username, password=DEFAULT_PW):
    if hasattr(user_or_username, "username"):
        return client.login(username=user_or_username.username, password=password)
    return client.login(username=user_or_username, password=password)

def upload_pdf(file_name="test.pdf", content=b"%PDF-1.4\n%..."):
    return SimpleUploadedFile(file_name, content, content_type="application/pdf")

def create_book(user, title="Test Book", author="Anon", genre=None, mood=None, status="to_read", create_ebook=True):
    def norm(x):
        if x is None: 
            return ""
        if isinstance(x, (list, tuple)):
            return ", ".join([str(i).strip() for i in x if str(i).strip()])
        return str(x).strip()

    book = Book.objects.create(
        title=title,
        author=author,
        added_by=user,
        genre=norm(genre),
        mood=norm(mood),
        status=status,
    )
    if create_ebook:
        ef, _ = EbookFile.objects.get_or_create(book=book)
        if not ef.file:
            ef.file = upload_pdf('auto.pdf')
            ef.save()
    return book

def make_image_file(name='img.png', size=(1,1), color=(255,0,0,255)):
    file = BytesIO()
    Image.new('RGBA', size, color).save(file, 'PNG')
    file.seek(0)
    return SimpleUploadedFile(name, file.read(), content_type='image/png')