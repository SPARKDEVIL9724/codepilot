from rest_framework import serializers
from .models import Project
from django.db.models import Q
from django.contrib.auth import authenticate

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "github_url"]
        