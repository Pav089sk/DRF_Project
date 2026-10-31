from django.urls import path, include
from users.views import ProfileView, PaymentViewSet, RegisterView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),

]

