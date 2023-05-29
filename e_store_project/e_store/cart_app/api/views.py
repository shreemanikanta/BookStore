from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from book_store_app.api.authentication import JWTAuthentication
from cart_app.api.serializers import CartItemSerializer
from cart_app.api.service import (list_books_in_cart,
                                  create_orders,
                                  get_ordered_books)


class CartApiView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        A function to list of books from the user's cart.
        """
        user = request.user
        response = list_books_in_cart(user, request)
        return response

    serializer_class = CartItemSerializer

    def delete(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.delete(request)
        return response


class CheckoutAPIView(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Get the books in the user's cart that have not been confirmed and
        return their information. The method retrieves the user's cart ID and
        the usercart_books that have not been confirmed. If there are no books
        in the user's cart that have not been confirmed, the method returns a
        response with an error message and HTTP status 400. Otherwise,
        the method creates a list of books and their information,
        including their ID, name, quantity, price, and sub-total. The method
        returns a response with the list of placed books and HTTP status 200.
        """
        user = request.user
        response = list_books_in_cart(user, request)
        return response

    def post(self, request):
        """
        Process the checkout request for the authenticated user

        Orders for all the items in the user's cart are created
        and saved in the Orders table.The status has set to confirmed
        for all items in the UserCart table for the given cart.

        Returns:
            A Response object with a success message and HTTP status 200
        """
        user = request.user
        try:
            success, message = create_orders(user)
            if success:
                return Response(message, status=status.HTTP_200_OK)
            else:
                return Response(message, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class MyOrdersAPI(APIView):
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        """
        Retrieves all the orders made by the authenticated user and
        returns them in a response.

        Returns:
            A Response object with a list of ordered books details
            and HTTP status 200
        """
        user = request.user
        try:
            success, response_data = get_ordered_books(user, request)
            if success:
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response(response_data,
                                status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
