from workspaces.models import Workspace
from projects.models import Project
from .models import Document
from .serializers import DocumentSerializer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

class DocumentListCreateView(ListCreateAPIView):
    serializer_class = DocumentSerializer
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
                user = self.request.user
            ).exists()
        ):
            raise PermissionDenied("User cannot access documents")
        return Document.objects.filter(project=project)


    def perform_create(self, serializer):
        project = self.get_project()
        if not(
            self.request.user == project.owner
            or project.members.filter(
                user = self.request.user
            ).exists()
        ):
            raise PermissionDenied("Only project owner or members can create Markdown")
        serializer.save(
            creator = self.request.user,
            project = project,
        )

class DocumentDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "document_id"

    def get_queryset(self):
        workspace = get_object_or_404(
            Workspace,
            id=self.kwargs["workspace_id"]
        )
        project = get_object_or_404(
            Project,
            id=self.kwargs["project_id"],
            workspace=workspace
        )

        if not (
            self.request.user == project.owner
            or project.members.filter(
                    user = self.request.user
            ).exists()
        ):
            raise PermissionDenied("User cannot access documents")
        return Document.objects.filter(project=project)

    def perform_update(self, serializer):
        if serializer.instance.creator != self.request.user:
            raise PermissionDenied("Only document owner can update documents")
        serializer.save()

    def perform_destroy(self, instance):
        if not (
            instance.creator == self.request.user
            or instance.project.owner == self.request.user
        ):
            raise PermissionDenied("Only project owner or document creator can delete a markdown")
        instance.delete()