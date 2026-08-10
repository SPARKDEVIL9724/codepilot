from django.db import models
from django.conf import settings

class Project(models.Model):

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank = True)
    github_url = models.URLField(blank=True)

    def __str__(self):
        return self.name