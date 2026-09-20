from projects.models import Project, ProjectMember
from .models import Task
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .serializers import TaskSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class TaskListCreateView(ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["project"]=get_object_or_404(Project, id=self.kwargs["project_id"])
        return context

    def get_queryset(self):
        return Task.objects.filter(project_id=self.kwargs["project_id"])

    def perform_create(self, serializer):
        project = get_object_or_404(Project, id = self.kwargs["project_id"])
        if not (
            self.request.user == project.owner 
            or ProjectMember.objects.filter(
                project=project,
                user=self.request.user,
                role="DEVELOPER",
                ).exists()
        ):
            raise PermissionDenied("You cannot create tasks in this project")
        serializer.save(project=project, created_by=self.request.user)