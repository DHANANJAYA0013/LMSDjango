from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('book/', views.book_list, name='book_list'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('Library/', views.Library, name='Library'),
    path('search/', views.search_books, name='search_books'),
    path('borrow/<int:book_id>/', views.borrow_book, name='borrow_book'),  # Borrow a book
    path('return/<int:loan_id>/', views.return_book, name='return_book'),  # Return a book
    path('loan_history/', views.loan_history, name='loan_history'),  # View loan history
    path('profile/', views.profile_view, name='profile'),

]


