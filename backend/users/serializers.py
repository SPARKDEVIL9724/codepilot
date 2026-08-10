from rest_framework import serializers
from .models import User
from django.db.models import Q
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "password", "github_username", "tech_stack"]

        extra_kwargs = {
            "password": {"write_only": True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        identifier = attrs["identifier"]
        password = attrs.pop("password")
        user = None

        try:
            user = User.objects.get(Q(username = identifier) | Q(email = identifier))
        except User.DoesNotExist:
            raise serializers.ValidationError("Invalid Credentials")
        
        user = authenticate(username=user.username,password=password)
        if user is None:
            raise serializers.ValidationError("Invalid Credentials")

        attrs["user"] = user
        return attrs

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email", "github_username", "tech_stack"]
        
