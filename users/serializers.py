from rest_framework import serializers
from django.contrib.auth import get_user_model
from users.models import Payment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'tel', 'city', 'avatar']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'pay_date', 'summ_pay',
            'paid_course', 'paid_lesson', 'payment_method'
        ]

class RegisterUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email', 'password', 'tel', 'city', 'avatar']

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)
