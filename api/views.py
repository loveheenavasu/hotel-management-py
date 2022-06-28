from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import *
from .models import *
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.views import TokenObtainPairView
from django.db.models import Q
from rest_framework.views import APIView
from django.http import Http404
from rest_framework.response import Response
# User Sign-up API
class UserViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    serializer_class = UserSerializer


# User Login API
class MyTokenObtainPairView(TokenObtainPairView):
    permission_classes = (AllowAny,)
    serializer_class = MyTokenObtainPairSerializer


class RoleViewSet(ModelViewSet):
    permission_classes = (AllowAny,)
    queryset = Role.objects.all()
    serializer_class = RoleSerializer







