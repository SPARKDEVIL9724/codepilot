from django.db import models
from django.conf import settings
from projects.models import Project

class CodeSnippet(models.Model):
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="code_snippets")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="code_snippets")
    title = models.CharField(max_length=50)
    language = models.CharField(max_length=30, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)