from django.contrib import admin
from .models import User,Book,Loan


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'date_joined')  # Add or modify fields here
    search_fields = ('username', 'email')  # Allow search by username and email
    list_filter = ('date_joined',)  # Add filters by date
    ordering = ('-date_joined',)  # Order by date_joined in descending order

    fields = ('username', 'email', 'password', 'date_joined')  # Add all the fields you want
    readonly_fields = ('date_joined',)  # Make certain fields read-only if desired

admin.site.register(User, UserAdmin)


class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'available', 'image')
    list_filter = ('available', 'genre')
    search_fields = ('title', 'author')
    ordering = ('title',)
    fields = ('title', 'author', 'genre', 'available', 'image')
    save_on_top = True

admin.site.register(Book, BookAdmin)


# Customizing the Loan admin interface
class LoanAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'due_date', 'return_date', 'is_returned', 'fine')
    search_fields = ('book__title', 'user__username')  # Search by book title and user
    list_filter = ('is_returned', 'due_date')  # Filter by return status and due date
    fields = ('book', 'user', 'due_date', 'return_date', 'is_returned', 'fine')

    def fine(self, obj):
        return obj.calculate_fine()  # Show the fine value for the loan
    fine.short_description = 'Fine ($)'

admin.site.register(Loan, LoanAdmin)
