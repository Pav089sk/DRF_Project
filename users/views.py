from rest_framework.generics import RetrieveUpdateAPIView
from django.contrib.auth import get_user_model
from users.serializers import UserSerializer

User = get_user_model()

class ProfileView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def get_object(self):
        return self.request.user

