from django.shortcuts import render
from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    model = User