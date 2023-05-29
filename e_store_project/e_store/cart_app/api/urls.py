from django.urls import path
from cart_app.api.views import CartApiView, CheckoutAPIView, MyOrdersAPI


urlpatterns = [
    path('cart_books/', CartApiView.as_view(), name='remove_book'),
    path('checkout/', CheckoutAPIView.as_view(), name='checkout'),
    path('my_orders/', MyOrdersAPI.as_view(), name='checkout'),
]
