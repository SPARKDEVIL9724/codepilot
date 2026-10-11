from rest_framework import serializers
from .models import AIReview

class AIReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIReview
        fields = [
            "id",
            "snippet",
            "findings",
            "summary",
            "timestamp",
        ]

        read_only_fields = [
            "id",
            "snippet",
            "findings",
            "summary",
            "timestamp",
        ]