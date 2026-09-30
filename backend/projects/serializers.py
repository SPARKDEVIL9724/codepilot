from rest_framework import serializers
from .models import Project, ProjectMember

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "workspace", "owner", "name", "description", "github_url"]
        read_only_fields = ["id", "workspace", "owner"]

class ProjectMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectMember
        fields = ["id", "user", "role"]
        read_only_fields = ["id","project"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.context["request"].method in ["PATCH", "PUT"]:
            self.fields["user"].read_only = True