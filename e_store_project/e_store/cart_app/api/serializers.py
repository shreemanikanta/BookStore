from rest_framework import serializers
from cart_app.models import UserCart
from book_store_app.models import Books
from rest_framework.response import Response
from rest_framework import status


class UserCartBookListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserCart
        fields = '__all__'


class BookImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Books
        fields = ['image']


class CartItemSerializer(serializers.Serializer):
    book_id = serializers.IntegerField()

    def delete(self, request):
        """
        A function to remove a product from the user's cart.
        """
        book_id = self.validated_data.get('book_id')
        user = request.user
        try:
            book = Books.objects.get(id=book_id)
        except Books.DoesNotExist:
            return Response({'message': 'Book is not available'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            cart = user.carts.latest('time_stamp')
            cart_item = cart.user_carts.get(book_id=book_id, confirmed=False)
            book.quantity += cart_item.quantity
            book.save()
        except UserCart.DoesNotExist:
            return Response({'message': 'Book not available in cart'},
                            status=status.HTTP_400_BAD_REQUEST)
        cart_item.delete()
        return Response({'message': f'{book.title} book deleted from cart'},
                        status=status.HTTP_200_OK)
