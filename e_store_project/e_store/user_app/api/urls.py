from django.urls import path
from user_app.api.views import RegistrationView, LoginView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
