from django.shortcuts import render
from django.shortcuts import get_object_or_404
from store.models import *
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import date
def index(request):
    return render(request, 'store/index.html')

def bookDetailView(request, bid):
    template_name = 'store/book_detail.html'
    book = Book.objects.get(id=bid)
    i=0
    for b in BookCopy.objects.filter(book=book):
        if b.status:
            i+=1
    context = {
        'book': book,
        'num_available': i,
    }
    return render(request, template_name, context=context)


@csrf_exempt
def bookListView(request):
    template_name = 'store/book_list.html'
    # Searching 
    bookdata = Book.objects.all()
    get_data = request.GET
    some= get_data.keys()
    if (len(some)!=0):
        if get_data['title'] =='' :
            if get_data['author']=='' :
                if get_data['genre']=='' :
                    bookdata = Book.objects.all()
                else: 
                    bookdata = Book.objects.filter(genre=get_data['genre'])
            else:
                if get_data['genre']=='' :
                    bookdata = Book.objects.filter(author=get_data['author'])
                else: 
                    bookdata = Book.objects.filter(genre=get_data['genre'],author=get_data['author'])
        else:
            if get_data['author']=='' :
                if get_data['genre']=='' :
                    bookdata = Book.objects.filter(title=get_data['title'])
                else: 
                    bookdata = Book.objects.filter(genre=get_data['genre'],title=get_data['title'])
            else:
                if get_data['genre']=='' :
                    bookdata = Book.objects.filter(author=get_data['author'],title=get_data['title'])
                else: 
                    bookdata = Book.objects.filter(genre=get_data['genre'],author=get_data['author'],title=get_data['title'])
            
    context = {
        'books': bookdata,
    }
    return render(request, template_name, context=context)

@login_required
def viewLoanedBooks(request):
    template_name = 'store/loaned_books.html'
    if request.user.is_authenticated:
        books = BookCopy.objects.filter(borrower=request.user)
    context = {
        'books': books,
    }
    return render(request, template_name, context=context)

@csrf_exempt
@login_required
def loanBookView(request):
    book_id = request.POST.get('bid')
    availBooks=BookCopy.objects.filter(book=Book.objects.get(id=book_id),status=True)
    print(len(availBooks))
    if len(availBooks)!=0:
        booktoget = availBooks.first()
        booktoget.status=False
        booktoget.borrow_date=date.today()
        booktoget.borrower=request.user
        booktoget.save(update_fields=['status','borrow_date','borrower'])
        response_data = {
            'message': 'success',
        }
    else:
        response_data = {
            'message': 'failure',
        }
    return JsonResponse(response_data)

@csrf_exempt
@login_required
def returnBookView(request):
    bcid = request.POST.get('bcid')
    booktoret = BookCopy.objects.get(id=bcid)
    booktoret.status=True
    booktoret.borrower = None
    booktoret.borrow_date=None
    booktoret.save(update_fields=['status','borrower','borrow_date'])
    response_data = {
            'message': 'success',
        }
    return JsonResponse(response_data)


