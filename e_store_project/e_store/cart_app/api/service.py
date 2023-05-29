from rest_framework import status
from rest_framework.response import Response
from cart_app.models import UserCart, Orders
from .serializers import BookImageSerializer
from django.db.models import Sum


def list_books_in_cart(user, request):
    try:
        cart = user.carts.filter(user_carts__confirmed=False).first()
        if not cart:
            return Response(
                {'message': 'Your cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        usercart_books = cart.user_carts.filter(confirmed=False)
        books = []
        if not usercart_books:
            return Response(
                {'message': 'Your cart is empty'},
                status=status.HTTP_400_BAD_REQUEST
            )
        for usercart_book in usercart_books:
            book = usercart_book.book
            image = BookImageSerializer(book, context={"request": request})
            book_data = {
                'id': book.id,
                'name': book.title,
                'quantity': usercart_book.quantity,
                'price': book.price,
                'sub_total': usercart_book.sub_total
            }
            book_data['image'] = image.data['image']
            books.append(book_data)
        total = (
                    cart.user_carts.
                    filter(confirmed=False).
                    values_list('sub_total', flat=True)
                )
        total = sum(total)
        response_data = {
            'usercart_books': books,
            'grand_total': total,
            'user': user.first_name,
            'email': user.email
        }
        return Response(response_data, status=status.HTTP_200_OK)

    except UserCart.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)


def create_orders(user):
    try:
        user_carts = (
                        user.carts
                        .latest('time_stamp')
                        .user_carts
                        .filter(confirmed=False)
                        .order_by('-time_stamp')
                    )
        total = user_carts.aggregate(total=Sum('sub_total')).get('total')
        for user_cart in user_carts:
            Orders.objects.create(
                                    user=user,
                                    book=user_cart.book,
                                    usercart=user_cart,
                                    total_price=user_cart.sub_total,
                                    status="Confirmed"
                                )
            user_cart.confirmed = True
            user_cart.save()
        return True, 'Ordered Successfully'

    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def get_ordered_books(user, request):
    try:
        ordered_books = (Orders.objects.
                         filter(user=user).order_by('-ordered_date'))
        books = []
        for ordered_book in ordered_books:
            book = ordered_book.book
            image = BookImageSerializer(book, context={"request": request})
            usercart = ordered_book.usercart
            book_data = {
                'id': book.id,
                'name': book.title,
                'quantity': usercart.quantity,
                'ordered_date': ordered_book.ordered_date,
                'image': book.image,
                'status': ordered_book.status,
                'price': book.price,
                'sub_total': ordered_book.total_price
            }
            book_data['image'] = image.data['image']
            books.append(book_data)
        response_data = {
            'ordered_books': books,
        }
        return True, response_data
    except Exception as e:
        return Response({'error': str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)
