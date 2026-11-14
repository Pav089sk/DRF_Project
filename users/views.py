from django.contrib.auth import get_user_model
from users.serializers import UserSerializer, PaymentSerializer
from users.models import Payment
from rest_framework import viewsets, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, ListAPIView
from users.serializers import RegisterUserSerializer
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny
from users.permissions import IsModerator
from users.services import create_stripe_product, create_stripe_price, create_stripe_checkout_session
from materials.models import Course
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response

User = get_user_model()

class ProfileView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user


class RegisterView(CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('user', 'paid_course', 'paid_lesson').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['pay_date']
    ordering = ['-pay_date']

    @action(detail=False, methods=['post'])
    def buy(self, request):
        course_id = request.data.get('course')
        course = get_object_or_404(Course, id=course_id)
        payment = Payment.objects.create(
            user=request.user,
            paid_course=course,
            summ_pay=course.price,
            payment_method=Payment.ONLINE,
        )

        product = create_stripe_product(course)
        price = create_stripe_price(product, course.price)
        session_id, session_url = create_stripe_checkout_session(price)
        payment.stripe_session_id = session_id
        payment.url_session = session_url
        payment.save()

        return Response({'payment_url': session_url}, status=status.HTTP_201_CREATED)


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsModerator]

