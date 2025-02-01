from django.shortcuts import render,HttpResponse
from .models import Book,Loan,User
from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from datetime import timedelta

from django.db.models import Q  # Import Q to use complex queries

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from .forms import SignupForm, LoginForm
# from .models import User
# from django.contrib.auth import authenticate, login

def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            password_confirm = form.cleaned_data['password_confirm']

            # Check if password and confirmation match
            if password != password_confirm:
                messages.error(request, "Passwords do not match!")
                return redirect('signup')

            # Check if username already exists
            if User.objects.filter(username=username).exists():
                messages.error(request, "Username already taken!")
                return redirect('signup')

            # Check if email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "Email already in use!")
                return redirect('signup')

            # Create the new user
            user = User.objects.create(username=username, email=email, password=password)
            messages.success(request, "Account created successfully! Please log in.")
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})



def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            # Check credentials manually
            try:
                user = User.objects.get(username=username)
                if user.password == password:
                    request.session['user_id'] = user.id  # Storing user ID in session
                    messages.success(request, "Logged in successfully!")
                    return redirect('Library')  # Redirect to home or any other page
                else:
                    messages.error(request, "Incorrect password!")
            except User.DoesNotExist:
                messages.error(request, "User does not exist!")

    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def index(request):
    return render(request, 'index.html')



def logout_view(request):
    try:
        del request.session['user_id']
    except KeyError:
        pass  # If the user is not logged in, it does nothing
    return render(request, 'index.html')


def Library(request):
    return render(request, 'Library.html')


def search_books(request):
    query = request.GET.get('query', '')  # Get the search query from the request
    books = Book.objects.filter(title__icontains=query) | Book.objects.filter(author__icontains=query) | Book.objects.filter(genre__icontains=query)
    return render(request, 'book_list.html', {'books': books, 'query': query})


def book_list(request):
    search_query = request.GET.get('search_query', '')
    
    # Filter books based on the search query
    if search_query:
        books = Book.objects.filter(
            Q(title__icontains=search_query) |
            Q(author__icontains=search_query) |
            Q(genre__icontains=search_query)
        )
    else:
        books = Book.objects.all()  # Show all books if no search query

    return render(request, 'book_list.html', {'books': books, 'search_query': search_query})




# Borrow a book
# @login_required
def borrow_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)

    if book.available:
        # Mark the book as unavailable
        book.available = False
        book.save()

        due_date = timezone.now().date() + timedelta(days=14)

        # Use the currently logged-in user
        user = User.objects.get(id=request.session.get('user_id'))

        # Create a loan entry for the borrowed book
        loan = Loan.objects.create(
            book=book,
            user=user,  
            due_date=due_date
        )

        # Constructing a HTML response with a success message
        response_text = f"""
        <html>
            <body>
                <h1>Success</h1>
                <p>{user.username} have borrowed <strong>{book.title}</strong>. Please return it by <strong>{due_date}</strong>.</p>
                <form action="/book" method="get">
                    <button type="submit">Go to Book List</button>
                </form>
            </body>
        </html>
        """
        return HttpResponse(response_text)

    else:
        response_text = f"""
        <html>
            <body>
                <h1>Error</h1>
                <p><strong>{book.title}</strong> is currently unavailable.</p>
                <form action="/book" method="get">
                    <button type="submit">Go to Book List</button>
                </form>
            </body>
        </html>
        """
        return HttpResponse(response_text)




# @login_required
def return_book(request, loan_id):
    loan = get_object_or_404(Loan, pk=loan_id, user=User.objects.get(id=request.session.get('user_id')))

    loan.is_returned = True
    loan.return_date = timezone.now().date()
    loan.book.available = True  # Mark the book as available again
    loan.book.save()  # Save the book's new availability status
    loan.save()  # Save the loan record with the return date

    messages.success(request, f"You have successfully returned '{loan.book.title}'.")
    return redirect('loan_history')  # Redirect back to the profile page


# @login_required
def loan_history(request):
    loans = Loan.objects.filter(user= User.objects.get(id=request.session.get('user_id'))).order_by('-due_date')  # Fetch the user's loans

    return render(request, 'loan_history.html', {'loans': loans})

# @login_required
def profile_view(request):
    user = User.objects.get(id=request.session.get('user_id'))

    loans = Loan.objects.filter(user= User.objects.get(id=request.session.get('user_id')), is_returned=False)  # Only borrowed books

    return render(request, 'profile.html', {'user': user,'loans': loans})  # Pass 'user' to the template


