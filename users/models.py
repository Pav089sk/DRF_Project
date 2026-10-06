from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватарка', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'