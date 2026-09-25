from projects.models import Project, ProjectMember
from .models import Task
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError
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
        project = get_object_or_404(Project, id=self.kwargs["project_id"])
        if not(
            self.request.user == project.owner
            or ProjectMember.objects.filter(
                project=project, 
                user=self.request.user
                ).exists()
            ):
            raise PermissionDenied("You are not a member of this project")

        tasks = Task.objects.filter(project=project)

        status = self.request.query_params.get("status")
        assignee = self.request.query_params.get("assigned_to")
        search_title = self.request.query_params.get("search")

        if status is not None:
            valid_statuses = [choice[0] for choice in Task.status_choices]
            if status not in valid_statuses:
                raise ValidationError("Invalid task status")
            tasks = tasks.filter(status=status)

        if assignee is not None:
            try:
                assignee = int(assignee)
                tasks = tasks.filter(assigned_to=assignee)
            except ValueError:
                raise ValidationError("assigned_to must be a valid member Id")
        
        if search_title is not None:
            tasks = tasks.filter(title__icontains=search_title)
        
        return tasks

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

class TaskDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(Project, id = self.kwargs["project_id"])
        if not(
            self.request.user == project.owner
            or ProjectMember.objects.filter(
                project=project, 
                user=self.request.user
                ).exists()
            ):
            raise PermissionDenied("You are not a member of this project")

        return Task.objects.filter(
            id=self.kwargs["task_id"], 
            project=project
            )

    def perform_update(self, serializer):
        task = self.get_object()
        current_user = self.request.user
        if not(
            current_user == task.project.owner
            or current_user == task.created_by
            or current_user == (task.assigned_to and task.assigned_to.user)
        ):
            raise PermissionDenied("User is not authorized to update this task")
        
        serializer.save()
        
    def perform_destroy(self, instance):
        current_user = self.request.user
        if not(
            current_user == instance.project.owner
            or current_user == instance.created_by
        ):
            raise PermissionDenied("User is not authorized to delete this task")
        instance.delete()