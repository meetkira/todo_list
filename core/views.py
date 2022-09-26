from django.contrib.auth import logout, login
from django.http import HttpResponse

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView, \
    GenericAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from core.models import User
from core.serializers import UserRegistrationSerializer, ProfileSerializer, ChangePasswordSerializer, LoginSerializer


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class ProfileView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ProfileSerializer

    def get_object(self):
        obj = self.request.user
        return obj

    def delete(self, request, *args, **kwargs):
        logout(request)
        try:
            del request.session['is_login']
        except KeyError:
            pass
        return Response({})


class ChangePasswordView(UpdateAPIView):
    model = User
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj


class LoginView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer: LoginSerializer = self.get_serializer(data=request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        request.session['is_login'] = 'true'
        request.session['username'] = user.username
        login(request, user=user)
        user_serializer = ProfileSerializer(instance=user)
        return Response(user_serializer.data)
