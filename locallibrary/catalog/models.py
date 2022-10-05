from django.db import models
from django.urls import reverse #Used to generate URLs by reversing the URL patterns
import uuid # Required for unique book instances
from django.contrib.auth.models import User
from datetime import date

class Genre(models.Model):
    """
    Model representing a book genre (e.g. Science Fiction, Non Fiction)
    """
    name = models.CharField(max_length=200, help_text="Enter a book genre")

    def __str__(self):
        """
        String for representing the model object (in admin site etc.)
        """
        return self.name

class Book(models.Model):
    """
    Model representing a book (but not a specify copy of book)
    """
    title = models.CharField(max_length=200)
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)
    # ForeignKey used because book can only have 1 author, but authors can have multiple books.
    # Author as string rather than object because it hasn't been declared yet in the file.
    summary = models.TextField(max_length=1000, help_text="Enter a brief description of the book")
    isbn = models.CharField('ISBN', max_length=13, help_text="13 characters")
    genre = models.ManyToManyField(Genre, help_text="Select a genre of this book")
    # ManyToManyField used because genre can contains many books. Books can covers many genres.
    # Genre class has aready been defined so we can specify the object above

    # adding a language
    language = models.ForeignKey('Language', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['title', 'author']

    def __str__(self):
        """
        String for representing the Model object.
        """
        return self.title

    def get_absolute_url(self):
        """
        Return the url to access a particular book instance
        """
        return reverse('book-detail', args=[str(self.id)])

    def display_genre(self):
        """
        Creates a string for genre. This is required to display genre in admin
        """
        return ', '.join([ genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genre'

class BookInstance(models.Model):
    """
    Model representing a specific vopy of a book (i.e. it can be borrowed from the library)
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          help_text="Unique ID for this particular book across whole library",)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)

    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    LOAN_STATUS = (
        ('m', 'Maintaince'),
        ('o', 'On Loan'),
        ('a', 'Availible'),
        ('r', 'Reserved')
    )

    status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text="Book availability")

    class Meta:
        ordering = ["due_back"]
        permissions = (("can_mark_returned", "Set books as returned"),)

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        """
        String for representing the Model object
        """
        return '{0} {1}'.format(self.id,self.book.title)

class Author(models.Model):
    """
    Model representing an author
    """
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField(null=True, blank=True)
    date_of_death = models.DateField('died', null=True, blank=True)

    def get_absolute_url(self):
        """
        Returns the url to access a particular author instance
        """
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the model object
        """
        return "{0} {1}".format(self.first_name, self.last_name)

class Language(models.Model):
    """
    Presents a language (English, Polish, Ukranian, Russian etc.)
    """
    name = models.CharField(max_length=100, help_text="Enter a book language")

    def get_absolute_url(self):
        """
        Return the url to access a particular author instace
        """
        return reverse('language', args=[str(self.id)])

    def __str__(self):
        """
        String for representing the model object
        """
        return self.name