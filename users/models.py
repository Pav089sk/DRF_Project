from decimal import Decimal

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

from materials.models import Lesson, Course


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    tel = models.CharField(max_length=20, blank=True, null=True)
    city = models.CharField(max_length=25, blank=True)
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватарка', blank=True, null=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Payment(models.Model):
    CASH = 'cash'
    TRANSFER = 'transfer_bank_account'

    PAYMENT_METHOD_CHOICES =[(CASH, 'Оплата наличными'),
    (TRANSFER, 'Перевод на банковский счет'),]

    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='payments', verbose_name='Пользователь')
    pay_date = models.DateField(verbose_name='Дата оплаты')
    paid_lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, related_name='paid_lesson', verbose_name='Оплаченный урок', null=True, blank=True)
    paid_course = models.ForeignKey(Course, on_delete=models.SET_NULL, related_name='paid_course',
                                    verbose_name='Оплаченный курс', null=True, blank=True)
    summ_pay = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'), verbose_name='Сумма оплаты')
    payment_method = models.CharField(choices=PAYMENT_METHOD_CHOICES, max_length=30, verbose_name='Способ оплаты')

    def __str__(self):
        return f"Платёж #{self.id} от {self.user.email} на сумму {self.summ_pay}"
