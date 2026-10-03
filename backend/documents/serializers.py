from rest_framework import serializers
from .models import Document

class DocumentSerializer(serializers.ModelSerializer):

    def validate_file(self, value):
        if value.name[-3:].lower() != ".md":
            raise serializers.ValidationError("Invalid file type")
        return value

    class Meta:
        model = Document
        fields = ["id", "creator", "project", "created_at", "updated_at", "file"]
        read_only_fields = ["id", "creator", "project", "created_at", "updated_at"]
