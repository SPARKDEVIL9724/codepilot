from .models import User
from rest_framework.generics import CreateAPIView
from .serializers import UserSerializer, LoginSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class RegisterView(CreateAPIView):
    serializer_class = UserSerializer
    model = User

class LoginView(APIView):

    def post(self, request):
        serializer = LoginSerializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        refresh = RefreshToken.for_user(user)

        return Response({
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
        })

class MeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user

        return Response({
            "username": user.username,
            "email": user.email,
            "github_username": user.github_username,
            "tech_stack": user.tech_stack,
        })