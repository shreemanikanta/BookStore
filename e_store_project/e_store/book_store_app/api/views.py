from rest_framework.views import APIView
from rest_framework import status, generics, filters
from rest_framework.response import Response
from book_store_app.api.serializers import (BookListSerializer,
                                            LanguageSerializer)
from book_store_app.api.authentication import JWTAuthentication
from book_store_app.models import Books, Language
from .service import add_book, add_book_to_cart


class AddBookView(APIView):
    """
    API view to add a book to the book store.
    """
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        user = request.user
        result = add_book(request.data, user)
        if 'errors' in result:
            return Response(result, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(result, status=status.HTTP_200_OK)

    def get(self, request):
        language = Language.objects.all()
        serializer = LanguageSerializer(language, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HomePageBookListView(generics.ListAPIView):
    """
    API view to list all the books on the home page.
    """
    queryset = Books.objects.all()
    serializer_class = BookListSerializer


class BookDetailView(APIView):
    """
    API view to display the details of a specific book
    and to add a book to the cart.
    """
    authentication_classes = [JWTAuthentication]


    def get(self, request, pk):
        """
        Handle GET requests to retrieve the details of a specific book.
        """
        try:
            book = Books.objects.get(pk=pk)
        except Books.DoesNotExist:
            return Response({'Error': 'Not found'},
                            status=status.HTTP_404_NOT_FOUND)
        serializer = BookListSerializer(book)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddBookToCartView(APIView):
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        """
        Handle POST requests to add a book to the cart.
        """
        book_id = request.data.get('book_id')
        quantity = request.data.get('quantity')
        response = add_book_to_cart(request.user, book_id, quantity)
        return response


class SearchView(generics.ListAPIView):
    """
    A view for searching books by title or description.

    If the 'search' query parameter is present in the request, search for books
    by title first, then by description if no matching books are found. Return
    the serialized list of books using the 'BookListSerializer' serializer.

    Returns:
            QuerySet: The queryset of books matching the search query.
    """

    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)
        if Books.objects.filter(title__icontains=search_query).exists():
            self.queryset = Books.objects.filter(title__icontains=search_query)
            self.serializer_class = BookListSerializer
            
        else:
            self.queryset = Books.objects.filter(description__icontains=search_query)
            self.serializer_class = BookListSerializer
        return self.queryset
        
        
