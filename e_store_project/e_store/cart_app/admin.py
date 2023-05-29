from django.contrib import admin
from .models import Cart, UserCart

# Register your models here.
admin.site.register(Cart)
admin.site.register(UserCart)
