from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.contrib.auth.hashers import make_password


class ProfileManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if not email:
            raise ValueError('The Email field must be set')
        hashed_pwd = make_password(password, salt=None)
        user = self.model(
            username=username,
            password=hashed_pwd,
            email=self.normalize_email(email),
            **extra_fields
        )
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not email:
            raise ValueError('The Email field must be set')
        user = self.create_user(
            username=username,
            email=email,
            password=password,
            is_active=True,
            **extra_fields
        )
        user.save(using=self._db)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=False)
    email = models.CharField(max_length=50, unique=True, default='')
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='profile_set',  # Custom related_name
        related_query_name='profile'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='profile_set',  # Custom related_name
        related_query_name='profile'
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = ProfileManager()

    def __str__(self):
        return self.username


class File(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name="the_user")
    file = models.FileField(upload_to='file/', null=False, blank=False)

    def __str__(self):
        return self.user.username
