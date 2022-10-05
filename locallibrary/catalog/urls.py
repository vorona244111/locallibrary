from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # re_path() is using now instead of url()
    re_path(r'^books/$', views.BookListView.as_view(), name='books'),
    re_path(r'^authors/$', views.AuthorListView.as_view(), name='authors')

]
urlpatterns += [
    # comparison "true pattern" not just strings
    # this regular expression match every url adress that starts with book/ and after that follow 1 or more numbers
    # to symbol of end string $. while execution it captures numbers and give their to display function
    # as param with name pk
    # Option 1 as class
    re_path(r'^book/(?P<pk>\d+)$', views.BookDetailView.as_view(), name='book-detail'),
    # Option 2 as function
    # re_path(r'^book/(?P<pk>\d+)$', views.book_detail_view, name='book-detail')
    re_path(r'^author/(?P<pk>\d+)$', views.AuthorDetailView.as_view(), name='author-detail'),
    re_path(r'^mybooks/$', views.LoanedBooksByUserListView.as_view(), name='my-borrowed'),
    re_path(r'^manager/$', views.LoanedBooksLibraryManagerListView.as_view(), name='all-borrowed'),
    # Forms -> /catalog/book/<bookinstance id>/renew/   id -> pk (primary key)
    re_path(r'^book/(?P<pk>[-\w]+)/renew/$', views.renew_book_librarian, name="renew-book-librarian"),
    re_path(r'^author/create/$', views.AuthorCreate.as_view(), name='author_create'),
    re_path(r'^autor/(?P<pk>\d+)/update/$', views.AuthorUpdate.as_view(), name='author_update'),
    re_path(r'^autor/(?P<pk>\d+)/delete/$', views.AuthorDelete.as_view(), name='author_delete'),
    re_path(r'^book/create/$',views.BookCreate.as_view(), name='book_create'),
    re_path(r'^book/(?P<pk>\d+)/update/$',views.BookUpdate.as_view(), name='book_update'),
    re_path(r'^book/(?P<pk>\d+)/delete/$',views.BookDelete.as_view(), name='book_delete'),

]