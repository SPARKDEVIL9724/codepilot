from rest_framework import serializers
from .models import CodeSnippet

class CodeSnippetSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodeSnippet

        fields = [
            "id",
            "creator",
            "project",
            "title",
            "language",
            "content",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "creator",
            "project",
            "created_at",
            "updated_at",
        ]
        