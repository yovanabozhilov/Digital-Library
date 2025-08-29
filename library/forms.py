from django import forms
from .models import Book, EbookFile, Chapter

class BookForm(forms.ModelForm):
    PREDEFINED_GENRES = [
        ('Fantasy', 'Фентъзи'),
        ('Science Fiction', 'Научна фантастика'),
        ('Historical Fiction', 'Историческа художествена литература'),
        ('Literary Fiction', 'Художествена литература'),
        ('Psychological Fiction', 'Психологическа литература'),
        ('Philosophical Fiction', 'Философска литература'),
        ('Mystery', 'Мистерия'),
        ('Thriller', 'Трилър'),
        ('Romance', 'Романтика'),
        ('Horror', 'Ужаси'),
        ('Adventure', 'Приключенска'),
        ('Dystopian', 'Дистопия'),
        ('Children’s', 'Детска литература'),
        ('Fairy Tale', 'Приказки'),
        ('Classic', 'Класика'),
        ('Poetry', 'Поезия'),
        ('Drama', 'Драма'),
        ('Crime', 'Криминална литература'),
        ('Satire', 'Сатира'),
        ('Western', 'Уестърн'),
        ('Magical Realism', 'Магически реализъм'),
        ('Short Stories', 'Къси разкази'),
        ('Non-fiction', 'Нехудожествена литература'),
        ('Biography', 'Биография'),
        ('Autobiography', 'Автобиография'),
        ('Memoir', 'Мемоари'),
        ('Self-help', 'Самопомощ'),
        ('Spirituality', 'Духовност'),
        ('Health & Wellness', 'Здраве и уелнес'),
        ('Science', 'Наука'),
        ('History', 'История'),
        ('Travel', 'Пътешествия'),
        ('Humor', 'Хумор'),
        ('Business', 'Бизнес'),
        ('Politics', 'Политика'),
        ('Technology', 'Технологии'),
        ('Cookbook', 'Готварски книги'),
        ('Art', 'Изкуство'),
        ('Music', 'Музика'),
        ('Education', 'Образование'),
        ('Religion', 'Религия'),
        ('Parenting', 'Родителство'),
    ]

    PREDEFINED_LANGUAGES = [
        ('English', 'Английски'),
        ('Bulgarian', 'Български'),
        ('Serbian', 'Сръбски'),
        ('French', 'Френски'),
        ('German', 'Немски'),
        ('Spanish', 'Испански'),
        ('Russian', 'Руски'),
    ]


    PREDEFINED_MOODS = [
        ('Funny', 'Забавно'),
        ('Sad', 'Тъжно'),
        ('Dark', 'Мрачно'),
        ('Lighthearted', 'Безгрижно'),
        ('Suspenseful', 'Напрегнато'),
        ('Romantic', 'Романтично'),
        ('Adventurous', 'Приключенско'),
        ('Melancholic', 'Меланхолично'),
        ('Hopeful', 'Обнадеждаващо'),
        ('Inspiring', 'Вдъхновяващо'),
        ('Mysterious', 'Мистериозно'),
        ('Tense', 'Стегнато'),
        ('Eerie', 'Зловещо'),
        ('Tragic', 'Трагично'),
        ('Philosophical', 'Философско'),
        ('Empowering', 'Укрепващо'),
        ('Bittersweet', 'Горчиво-сладко'),
        ('Reflective', 'Размишляващо'),
        ('Chilling', 'Страховито'),
        ('Spiritual', 'Духовно'),
        ('Thought-provoking', 'Провокиращо размисъл'),
        ('Satirical', 'Сатирично'),
        ('Cynical', 'Цинично'),
        ('Uplifting', 'Ободряващо'),
        ('Energetic', 'Енергично'),
        ('Optimistic', 'Оптимистично'),
        ('Gritty', 'Сурово'),
        ('Nostalgic', 'Носталгично'),
        ('Magical', 'Магическо'),
        ('Playful', 'Игриво'),
    ]


    genre = forms.MultipleChoiceField(
        label='Жанр',
        choices=PREDEFINED_GENRES,
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'}),
        required=False,
    )

    language = forms.ChoiceField(
        label='Език',
        choices=[('', '--- Избери език ---')] + PREDEFINED_LANGUAGES
    )

    mood = forms.MultipleChoiceField(
        label='Настроение',
        choices=PREDEFINED_MOODS,
        widget=forms.SelectMultiple(attrs={'class': 'select2 form-control'}),
        required=False,
    )

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'mood', 'isbn', 'description', 'language', 'status', 'cover_image']
        labels = {
            'title': 'Заглавие',
            'author': 'Автор',
            'genre': 'Жанрове',
            'mood': 'Настроения',
            'isbn': 'ISBN',
            'description': 'Описание',
            'language': 'Език',
            'status': 'Статус',
            'cover_image': 'Корица:',
        }

    def clean_mood(self):
        moods = self.cleaned_data.get('mood', [])
        return ', '.join(moods)  
    
    def clean_genre(self):
        genres = self.cleaned_data.get('genre', [])
        return ', '.join(genres)  

class EbookFileForm(forms.ModelForm):
    class Meta:
        model = EbookFile
        fields = ['file']
        labels = {
            'file': 'Файл с книгата (PDF):',
        }

    def clean_file(self):
        file = self.cleaned_data['file']
        allowed_extensions = ['.pdf']
        if not any(file.name.lower().endswith(ext) for ext in allowed_extensions):
            raise forms.ValidationError("Позволени са само PDF файлове.")
        return file

class ChapterForm(forms.ModelForm):
    class Meta:
        model = Chapter
        fields = ['title', 'content']