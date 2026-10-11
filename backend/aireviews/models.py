from django.db import models
from codesnippets.models import CodeSnippet

class AIReview(models.Model):
    snippet = models.OneToOneField(
        CodeSnippet,
        on_delete=models.CASCADE,
        related_name="ai_review"
    )
    summary = models.TextField()
    findings = models.JSONField()
    timestamp = models.DateTimeField(auto_now=True)