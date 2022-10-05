from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre, Language

from django.http import Http404
from django.views import generic
from django.contrib.auth.decorators import login_required, permission_required # decorator @login_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin # class view login and permissions
# Form imports
from django.shortcuts import get_object_or_404 # return object from model with pk or give 404
from django.http import HttpResponseRedirect # This class redirect to another address (http 302)
from django.urls import reverse # generate url address with url config and additional arguments
# Author view
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
import datetime

from .forms import RenewBookForm


class BookListView(generic.ListView):
    model = Book
    # My own var name. default - book_list (object_list)
    context_object_name = 'book_list'
    # getting 5 books that contains word in title. we also can rewrite qet_queryset bewlow          #same
    ### queryset = Book.objects.filter(title__icontains="мед")[:5]
    # Using my template. by default ("/locallibrary/catalog/templates/catalog/book_list.html")
    template_name = 'my_books_list.html'
    # Page view
    paginate_by = 10

    ### def get_queryset(self):
    ###     return Book.objects.filter(title__icontains="мед")[:5]                                       #same

    #rewriting method get_context_data to give template another vars
    # 1-st getting real context from our superclass!
    # 2-nd adding into context some data
    # 3-st return our new context
    def get_context_data(self, *, object_list=None, **kwargs):
        # first getting base realisation of context
        context = super(BookListView, self).get_context_data(**kwargs)
        # adding new var to context and initialise her some value
        context['some data'] = 'this is just some data'
        return context

#================================================================================================================
# Create your views here.
def index(request):
    """
    Function that display home page of website
    """
    # display tilte
    title = "Locallib"
    # Generate 'count' of few main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Availible books status = 'a'

    num_instances_availible = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count() # method all() is used by default

    # task: modify func to display count of genres and books that includes in titles some text
    num_books_with_text = Book.objects.filter(title__icontains="Медв").count()
    num_genres_with_text = Genre.objects.filter(name__icontains='русс').count()

    # Sessions
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    # Drawing html index.html with data inside
    # Using var context
    return render(
        request,
        'index.html',
        context=
        {
            'num_books':num_books,
            'num_instances':num_instances,
            'num_instances_availible':num_instances_availible,
            'num_authors':num_authors,
            'title':title,
            'num_books_with_text': num_books_with_text,
            'num_genres_with_text': num_genres_with_text,
            'num_visits':num_visits,

        }
    )

#================================================================================================================\\
# Option 1

class BookDetailView(LoginRequiredMixin ,generic.DetailView):
    model = Book
    template_name = "book_detail.html"
    # LoginRequiredMixin alts
    # login_url = '/login/'
    # redirect_field_name = '/login/'

#-------------------------------
# Option 2
"""
def book_detail_view(request, pk):
    try:
        book_id = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        raise Http404("Book does not exist")
    
    # easy generation of 404 below
    # book_id=get_object_or_404(Book, pk=pk)

    return render(
        request,
        "book_detail.html",
        context={
            'book':book_id,
        }
    )
"""
class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 10
    template_name = 'authors_list.html'
    context_object_name = 'author_list'

class AuthorDetailView(generic.DetailView):
    model = Author
    template_name = 'author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """
    Generic class-based view listing books on loan to current user
    """
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')

class LoanedBooksLibraryManagerListView(PermissionRequiredMixin, generic.ListView):
    model = BookInstance
    template_name = 'bookinstance_list_borrowed_manager.html'
    # we need to check the permisson
    permission_required = 'catalog.can_mark_returned'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')

# Form
@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, pk):
    """
    View function for renewing a specific bookinstance by librarian
    """
    book_inst = get_object_or_404(BookInstance, pk=pk) # getting our object

    # If request is POST
    if request.method == 'POST':

        # Create new instance of form and fill data from request (bindings: связывание)
        form = RenewBookForm(request.POST)

        # check valid
        if form.is_valid():
            # processing data from form.cleaned_data as required (here we just write it to the model due_back field)
            book_inst.due_back = form.cleaned_data['renewal_date']
            book_inst.save()

            # Go to adress 'all-borrowed'
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If request is GET (or any other method)
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date,})

    # context already have object Book_instance

    return render(
        request,
        'book_renew_librarian.html',
        {
            'form':form,
            'bookinst':book_inst
        }
    )

class AuthorCreate(CreateView):
    model = Author
    fields = "__all__"
    initial = {'date_of_death': "12/10/2016"}
    template_name = "author_form.html"

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    template_name = 'author_form.html'

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    template_name = 'author_confirm_delete.html'

class BookCreate(CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book_form.html'

class BookUpdate(UpdateView):
    model = Book
    template_name = 'book_form.html'


class BookDelete(DeleteView):
    model = Book
    template_name = 'book_confirm_delete.html'
    success_url = reverse_lazy('books')