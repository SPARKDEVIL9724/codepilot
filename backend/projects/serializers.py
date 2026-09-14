from rest_framework import serializers
from .models import Project, ProjectMember
from django.db.models import Q
from django.contrib.auth import authenticate

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "github_url"]

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ["id", "user", "role"]
        read_only_fields = ["id"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context["request"].method in ["PATCH", "PUT"]:
            self.fields["user"].read_only = True