from django.contrib import admin
from .models import Genre, Book, BookInstance, Author, Language

class BookInline(admin.TabularInline):
    model = Book
    fields = ['title', 'language', 'isbn']

# Define admin class
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'date_of_birth', 'date_of_death')
    fields = ['first_name', 'last_name', ('date_of_birth', 'date_of_death')]
    inlines = (BookInline,)
# register admin class with the assosiated model
admin.site.register(Author, AuthorAdmin)

class BookInstanceInline(admin.TabularInline):
    model = BookInstance
    extra = 0




# Register the admin classes using decorator @admin.register
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'display_genre')
    inlines = [BookInstanceInline]
 #   exclude = ['isbn']

@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('id', "status", "borrower", 'due_back')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('book', 'imprint', 'id')
        }),
        ('Availability', {
            'fields': ('status', 'due_back')
        }),
        ('User', {
            'fields': ('borrower',)
        }
        )


    )

class BookInstanceInline(admin.TabularInline):
    model = BookInstance




# Register your models here.
#admin.site.register(Book)
#admin.site.register(Author)
#admin.site.register(BookInstance)
admin.site.register(Genre)
admin.site.register(Language)