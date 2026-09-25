from django.db import models
from tasks.models import Task
from django.conf import settings

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE,related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="created_comments")
    content = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.author} : {self.created_at}"