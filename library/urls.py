from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name='welcome'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('main/', views.main_page, name='main'),
    path('profile/', views.profile_page, name='profile'),

    path('books/add/', views.add_book, name='add_book'),
    path('my-added-books/', views.my_added_books, name='my_added_books'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),

    path('book/<int:book_id>/read/', views.read_book, name='read_book'),
    path('book/<int:book_id>/pdf/', views.read_ebook, name='read_ebook'),

    path('book/<int:book_id>/', views.book_detail, name='book_detail'),

    path('books/<int:book_id>/save_duration/', views.save_reading_duration, name='save_reading_duration'),

    path('mybooks/create/', views.create_mybook, name='create_mybook'),
    path('mybooks/<int:book_id>/', views.view_mybook, name='view_mybook'),
    path('mybooks/<int:book_id>/delete/', views.delete_mybook, name='delete_mybook'),
    path('mybooks/<int:book_id>/add-chapter/', views.add_chapter, name='add_chapter'),
    path('mybooks/<int:book_id>/chapter/<int:chapter_id>/edit/', views.edit_chapter, name='edit_chapter'),
    path('mybook/<int:book_id>/chapter/<int:chapter_id>/delete/', views.delete_chapter, name='delete_chapter'),
    path('upload_image/', views.upload_image, name='upload_image'),

    path('mybook/<int:mybook_id>/export/docx/', views.export_mybook_docx, name='export_mybook_docx'),
    path('mybook/<int:mybook_id>/export/pdf/', views.export_mybook_pdf, name='export_mybook_pdf'),

    path('save-last-page/<int:book_id>/', views.save_last_page, name='save_last_page'),
    path('save_quote/', views.save_quote, name='save_quote'),
    path('save_note/', views.save_note, name='save_note'),
    path('delete_quote/', views.delete_quote, name='delete_quote'),
    path('delete_note/', views.delete_note, name='delete_note'),

    path('lookup/', views.lookup_word, name='lookup_word'),
    path("translate_define/", views.translate_and_define, name="translate_define"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)