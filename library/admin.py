from django.contrib import admin
from .models import (Book, Review, JournalEntry, EbookFile, MyBook, Chapter, WordLookup, ReadingSession, SavedQuote)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "genre", "mood", "status", "added_by")
    search_fields = ("title", "author", "isbn")
    list_filter = ("genre", "mood", "status")

@admin.register(MyBook)
class MyBookAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created")
    search_fields = ("title",)

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
    list_display = ("title", "mybook")
    search_fields = ("title",)

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "rating")
    search_fields = ("book__title", "user__username")

@admin.register(JournalEntry)
class JournalEntryAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "page", "created_at")
    search_fields = ("content", "book__title")
    list_filter = ("created_at",)

@admin.register(EbookFile)
class EbookFileAdmin(admin.ModelAdmin):
    list_display = ("book", "file")

@admin.register(WordLookup)
class WordLookupAdmin(admin.ModelAdmin):
    list_display = ('word', 'definition')
    search_fields = ('word',)

@admin.register(ReadingSession)
class ReadingSessionAdmin(admin.ModelAdmin):
    list_display = ("user", "book", "start_time", "end_time", "pages_read")
    list_filter = ("start_time",)

@admin.register(SavedQuote)
class SavedQuoteAdmin(admin.ModelAdmin):
    list_display = ("book", "user", "page", "quote_text", "created_at")
    search_fields = ("quote_text", "book__title")
    list_filter = ("created_at",)


