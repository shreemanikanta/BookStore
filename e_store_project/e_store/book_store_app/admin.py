from django.contrib import admin
from .models import Language, Books, BookLanguage

# Register your models here.
admin.site.register(Language)
admin.site.register(Books)
admin.site.register(BookLanguage)
