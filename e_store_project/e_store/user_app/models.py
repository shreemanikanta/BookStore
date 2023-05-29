from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser, PermissionsMixin)


class UserManager(BaseUserManager):
    """
    A custom user manager for the User model,
    Allows creating and managing users, including creating a superuser.
    """
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates a new user with the given email and password.
        """
        # if not email:  #review: want to validate in serializers
        #     raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates a new superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    """
    Model class for user roles.
    """
    role = models.CharField(max_length=8)

    def __str__(self):
        return self.role


class User(AbstractBaseUser, PermissionsMixin):
    """
    A custom user model.
    """
    username = models.CharField(max_length=40, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'email']

    objects = UserManager()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

    class Meta:
        db_table = 'users'


class UserRoles(models.Model):
    """
    This model represents the relationship between
    a user and their assigned role.
    It has two fields: a foreign key to the User model
    and a foreign key to the Role model.
    """
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='user_roles')
    role = models.ForeignKey(Role,
                             on_delete=models.CASCADE,
                             related_name='user_roles')

    def __str__(self):
        return "{} - {}".format(self.user.username, self.role)


class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500, unique=True)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token

    class Meta:
        ordering = ['-blacklisted_at']
        verbose_name_plural = 'Blacklisted Tokens'
