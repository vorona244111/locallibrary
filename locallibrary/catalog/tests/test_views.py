from django.test import TestCase
from catalog.models import Author, BookInstance, Book, Genre, Language
from django.urls import reverse
import uuid
import datetime
from django.utils import timezone
from django.contrib.auth.models import User # need to represent user as borrower
import random


class AuthorListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # creates 13 authors for pagination tests
        numbers_of_authors = 13
        for author_num in range(numbers_of_authors):
            Author.objects.create(first_name='Cristian{}'.format(author_num),last_name='Surname{}'.format(author_num))

    def test_view_url_exists_at_desired_location(self):
        resp = self.client.get('/catalog/authors/')
        self.assertEquals(resp.status_code, 200)


    def test_view_url_accessible_by_name(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'authors_list.html')

    def test_pagination_is_ten(self):
        resp = self.client.get(reverse('authors'))
        self.assertEquals(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 10)

    def test_list_all_authors(self):
        resp = self.client.get(reverse('authors')+'?page=2')
        self.assertEquals(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'] == True)
        self.assertTrue( len(resp.context['author_list']) == 3)

class LoanedBooksByUserListViewTest(TestCase):

    def setUp(self):
        # creating 2 users
        test_user1 = User.objects.create_user(username='testuser1', password='12345')
        test_user1.save()
        test_user2 = User.objects.create_user(username='testuser2', password='12345')
        test_user2.save()

        # creating a book
        test_author = Author.objects.create(first_name='Jonh', last_name='Smith')
        test_genre = Genre.objects.create(name='Fantasy')
        test_language = Language.objects.create(name='English')
        test_book = Book.objects.create(title='Book title', summary='My book summary', isbn='123456', author=test_author, language=test_language)
        # Create genre as pop-step
        genre_objects_for_book = Genre.objects.all()
        test_book.genre.set(genre_objects_for_book) # many-to-many type can't assingnment directly
        test_book.save()

        # creating 30 objects BookIntances
        number_of_book_copies = 30
        for book_copy in range(number_of_book_copies):
            return_date = timezone.now() + datetime.timedelta(days=book_copy%5)
            if book_copy % 2:
                the_borrower = test_user1
            else:
                the_borrower = test_user2
            status = 'm'
            BookInstance.objects.create(book=test_book,id = uuid.uuid4(),imprint='Unlikely Imprint, 2016', due_back=return_date, borrower=the_borrower, status=status)


    def test_redirect_if_not_logged(self):
        resp = self.client.get(reverse('my-borrowed'))
        self.assertRedirects(resp, '/accounts/login/?next=/catalog/mybooks/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(username= 'testuser1', password= '12345')
        resp = self.client.get(reverse('my-borrowed'))

        # Checking the login
        self.assertEquals(str(resp.context['user']), 'testuser1')
        # Checking answering the call
        self.assertEquals(resp.status_code, 200)

        # Checking that we used true template
        self.assertTemplateUsed(resp, 'bookinstance_list_borrowed_user.html')

    def test_only_borrowed_books_in_list(self):
        login = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEquals(str(resp.context['user']), 'testuser1')
        self.assertEquals(resp.status_code, 200)

        # Check that we do not have any instances
        self.assertTrue('bookinstance_list' in resp.context)
        self.assertEquals(len(resp.context['bookinstance_list']), 0)

        # Getting some books
        get_ten_books = BookInstance.objects.all()[:10]

        for copy in get_ten_books:
            copy.status = 'o'
            copy.save()

        resp = self.client.get(reverse('my-borrowed'))
        self.assertEquals(str(resp.context['user']), "testuser1")
        self.assertEquals(resp.status_code, 200)

        # Confirm that all books belongs testuser1 and OnLoan
        for bookitem in resp.context['bookinstance_list']:
            self.assertEquals(resp.context['user'], bookitem.borrower)
            self.assertEquals('o', bookitem.status)

    def test_pages_ordered_bu_due_date(self):

        for copy in BookInstance.objects.all():
            copy.status = 'o'
            copy.save()

        logging = self.client.login(username='testuser1', password='12345')
        resp = self.client.get(reverse('my-borrowed'))

        self.assertEquals(str(resp.context['user']), 'testuser1')
        self.assertEquals(resp.status_code, 200)

        # Checking that shows only 10 books
        self.assertEquals(len(resp.context['bookinstance_list']), 10)

        last_day = 0
        for copy in resp.context['bookinstance_list']:
            if last_day == 0:
                last_day = copy.due_back
            else:
                self.assertTrue(last_day <= copy.due_back )
