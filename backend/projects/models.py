from django.db import models
from django.conf import settings
from workspaces.models import Workspace

class Project(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name="projects")
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_projects")
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    github_url = models.URLField(blank=True)
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through="ProjectMember", related_name="member_projects")

    def __str__(self):
        return self.name

class ProjectMember(models.Model):
    ROLE_CHOICES = [
            ('DEVELOPER', 'Developer'),
            ('VIEWER', 'Viewer'),
        ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="project_memberships")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="VIEWER")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user","project"],
                name="unique_project_member"
            )
        ]

    def __str__(self):
        return f"{self.user} ({self.role})"