from book_store_app.models import Books, Language, BookLanguage
from rest_framework import status
from cart_app.models import Cart, UserCart
from .serializers import AddBookSerializer
from rest_framework.response import Response


def add_book(data, user):
    """
    API view to add a book to the book store.
    """
    serializer = AddBookSerializer(data=data)
    if serializer.is_valid():
        book = Books.objects.create(
            title=data.get('title'),
            description=data.get('description'),
            author=data.get('author'),
            added_quantity=data.get('quantity'),
            quantity=data.get('quantity'),
            price=data.get('price'),
            image=data.get('image'),
            user=user)
        language_id = data.get('language')
        language = Language.objects.get(id=language_id)
        BookLanguage.objects.create(book=book, language=language)
        return {'message': 'successfully added book', 'data': serializer.data}
    else:
        return serializer.errors


def add_book_to_cart(user, book_id, quantity):
    """
    Add a book to the cart for the given user with the given quantity.
    """
    try:
        book_obj = Books.objects.get(pk=book_id)
    except Books.DoesNotExist:
        return Response({'Error': 'Book not found'},
                        status=status.HTTP_404_NOT_FOUND)

    selected_quantity = int(quantity)
    book_obj.quantity = book_obj.quantity - selected_quantity
    book_obj.save()
    cart_obj, obj = Cart.objects.get_or_create(user=user)

    if UserCart.objects.filter(
                                book=book_obj,
                                cart__user=user,
                                confirmed=False
                                ).exists():
        usrcart_obj = UserCart.objects.get(book=book_obj,
                                           cart__user=user,
                                           confirmed=False)
        usrcart_obj.quantity = usrcart_obj.quantity + selected_quantity
        usrcart_obj.sub_total = usrcart_obj.quantity * usrcart_obj.book.price
        usrcart_obj.save()
        response_data = {
            'Book': book_obj.title,
            'Updated-Quantity': selected_quantity
        }
        return Response({'message': 'Updated Book quantity',
                         'Updated-Book': response_data},
                        status=status.HTTP_200_OK)

    else:
        usrcart_obj = UserCart.objects.create(
            book=book_obj,
            quantity=selected_quantity,
            sub_total=int(book_obj.price) * selected_quantity,
            cart=cart_obj,
            confirmed=False
        )
        response_data = {
            'Book': book_obj.title,
            'Added-Quantity': selected_quantity
        }
        return Response({'message': 'Added Book to cart',
                         'Added-Book': response_data},
                        status=status.HTTP_200_OK)
