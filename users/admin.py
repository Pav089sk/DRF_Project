from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser, Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'pay_date', 'summ_pay', 'payment_method', 'paid_course', 'paid_lesson')
    list_filter = ('payment_method', 'pay_date')
    search_fields = ('user__email',)
    readonly_fields = ('pay_date',)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    filter_horizontal = ()
    ordering = ('email',)
    list_display = ('email', 'city', 'is_staff', 'is_active')
    search_fields = ('email',)
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Личные данные', {'fields': ('tel', 'city', 'avatar')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
