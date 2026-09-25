from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["task", "author", "content", "created_at"]
        read_only_fields = ["task", "author", 'created_at']
