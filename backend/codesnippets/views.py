from .models import CodeSnippet
from .serializers import CodeSnippetSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from projects.models import Project
from workspaces.models import Workspace

class CodeSnippetListCreateView(ListCreateAPIView):
    serializer_class = CodeSnippetSerializer
    permission_classes = [IsAuthenticated]

    def get_project(self):
        workspace = get_object_or_404(
                        Workspace,
                        id=self.kwargs["workspace_id"]
                    )
        return get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace=workspace
        )

    def get_queryset(self):
        project = self.get_project()
        if not (
            self.request.user == project.owner
            or project.members.filter(
                user=self.request.user
            ).exists()
        ):
            raise PermissionDenied("User not a member of this project")
        return CodeSnippet.objects.filter(
            project=project
        )

    def perform_create(self, serializer):
        project = self.get_project()
        if not (
            self.request.user == project.owner
            or project.members.filter(
                user=self.request.user
            ).exists()
        ):
            raise PermissionDenied("Only project owner or members can create code snippets")
        serializer.save(
            creator=self.request.user,
            project=project
        )

class CodeSnippetDetailView(RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = "snippet_id"
    serializer_class = CodeSnippetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace=get_object_or_404(
                Workspace,
                id=self.kwargs["workspace_id"]
            )
        )

        if not (
            project.owner == self.request.user
            or project.members.filter(
                user=self.request.user
            ).exists()
        ):
            raise PermissionDenied("user not a member of this project")
        
        return CodeSnippet.objects.filter(
            project=project
            )

    def perform_update(self, serializer):
        snippet = serializer.instance
        if self.request.user != snippet.creator:
            raise PermissionDenied("only creator can modify snippet")
        serializer.save()

    def perform_destroy(self, instance):
        if not (
            self.request.user == instance.project.owner
            or self.request.user == instance.creator
        ):
            raise PermissionDenied("Only project owner or creator can delete snippet")
        instance.delete()