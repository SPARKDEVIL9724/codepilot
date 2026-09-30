from workspaces.models import Workspace
from .models import Project, ProjectMember
from .serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not (
            self.request.user == workspace.owner
            or workspace.members.filter(
                user=self.request.user,
            ).exists()
        ):
            raise PermissionDenied("You are not a member of this Workspace")
        return Project.objects.filter(workspace=workspace)

    def perform_create(self, serializer):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not (
            self.request.user == workspace.owner
            or workspace.members.filter(
                user=self.request.user,
                role="ADMIN"
            ).exists()
        ):
            raise PermissionDenied("You are not authorized to create project in this Workspace")
        serializer.save(workspace=workspace ,owner=self.request.user)

class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "project_id"

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not (
            self.request.user == workspace.owner
            or workspace.members.filter(
                user=self.request.user,
            ).exists()
        ):
            raise PermissionDenied("You are not a member of this Workspace")
        return Project.objects.filter(workspace=workspace)

    def perform_update(self, serializer):
        if self.request.user != serializer.instance.owner:
            raise PermissionDenied("You are not authorized to update this project")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.owner:
            raise PermissionDenied("You are not authorized to delete this project")
        instance.delete()

class ProjectMemberListCreateView(ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace_id=self.kwargs["workspace_id"]
        )
        if not (
            project.owner==self.request.user 
            or project.members.filter(
                user=self.request.user
            ).exists()
        ):
            raise PermissionDenied("You are not a member of this project")
        return ProjectMember.objects.filter(project=project)

    def perform_create(self, serializer):
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace_id=self.kwargs["workspace_id"]
        )
        if project.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this project")
        if not (
            project.workspace.members.filter(
                user=serializer.validated_data["user"]
            ).exists()
        ):
            raise ValidationError("Given user not a member of this workspace")
        serializer.save(project=project)

class ProjectMemberDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "member_id"
    
    def get_queryset(self):
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace_id=self.kwargs["workspace_id"]
        )
        if not (
            project.owner==self.request.user 
            or project.members.filter(
                user=self.request.user
            ).exists()
        ):
            raise PermissionDenied("You are not a member of this project")
        return ProjectMember.objects.filter(project=project)

    def perform_update(self, serializer):
        project = serializer.instance.project
        if self.request.user != project.owner:
            raise PermissionDenied("Only project owner can update member details")
        serializer.save()
    
    def perform_destroy(self, instance):
        project = instance.project
        if self.request.user != project.owner:
            raise PermissionDenied("Only project owner can delete a member")
        instance.delete()