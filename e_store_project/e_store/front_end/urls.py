from django.urls import path

from front_end.views import (
                            register, login, home_page, book_details,
                            add_book, cart, invoice, my_orders,
                            session_token, logout
                            )

app_name = 'front_end'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('register/', register, name='register'),
    path('home_page/', home_page, name='home_page'),
    path('book_details/<int:id>/', book_details, name='book_details'),
    path('add_book/', add_book, name='add_book'),
    path('cart/', cart, name='cart'),
    path('invoice/', invoice, name='invoice'),
    path('my_orders/', my_orders, name='my_orders'),
    path('session_token/', session_token, name='session_token'),
]
