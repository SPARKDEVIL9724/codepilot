from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["id","project", "title", "description", "created_at", "created_by", "status", "assigned_to"]
        read_only_fields = ["id", "created_by", "created_at", "project"]

    def validate_assigned_to(self, value):
        if value is None:
            return value

        project = self.context.get("project")

        if(project != value.project):
            raise serializers.ValidationError("Assigned member must belong to this project")
        return value