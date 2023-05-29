from django.urls import path
from book_store_app.api.views import (AddBookView,
                                      HomePageBookListView, BookDetailView,
                                      AddBookToCartView, SearchView)


urlpatterns = [
    path('add_book/', AddBookView.as_view(), name='add_book'),
    path('home_page/', HomePageBookListView.as_view(), name='home_page'),
    path('book_detail/<int:pk>/', BookDetailView.as_view(),
         name='book_details'),
    path('add_book_to_cart/', AddBookToCartView.as_view(),
         name='add_book_to_cart'),
    path('search/', SearchView.as_view(), name='search')
]
