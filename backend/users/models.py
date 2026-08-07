from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    github_username = models.CharField(max_length=50, blank=True)
    tech_stack = models.CharField(max_length=50, blank=True)

    def __str__(self):
        return self.username