from django.db import models
from user_app.models import User
from book_store_app.models import Books


class Cart(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='carts')
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(
                    str(self.user.id)
                    + "  -------  "
                    + self.user.first_name + ' '
                    + self.user.last_name + "  -------  " + "CART"
                    )


class UserCart(models.Model):
    cart = models.ForeignKey(Cart,
                             on_delete=models.CASCADE,
                             related_name='user_carts')
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    sub_total = models.IntegerField()
    confirmed = models.BooleanField(default=False)
    time_stamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.book.title + "  -------  " + (self.cart.user.first_name + " ------ " + str(self.cart.user.id))


class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Books, on_delete=models.CASCADE)
    usercart = models.ForeignKey(UserCart,
                                 on_delete=models.CASCADE,
                                 related_name='orders')
    ordered_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()
    status = models.CharField(max_length=100)
