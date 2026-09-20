from django.db import models
from django.conf import settings
from projects.models import Project, ProjectMember

class Task(models.Model):
    status_choices =[("TODO", "To Do"),("IN_PROGRESS", "In Progress"),("DONE", "Completed")]

    project = models.ForeignKey(Project ,on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,null=True, on_delete=models.SET_NULL, related_name="created_tasks")
    assigned_to = models.ForeignKey(ProjectMember,on_delete=models.SET_NULL, blank=True, null=True, related_name="assigned_tasks")
    status = models.CharField(max_length=20, choices=status_choices, default="TODO")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} : {self.status}"
    
