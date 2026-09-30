from .models import Workspace, WorkspaceMember
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .serializers import WorkspaceSerializer, WorkspaceMemberSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Q

class WorkspaceListCreateView(ListCreateAPIView):
    model = Workspace
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Workspace.objects.filter(
            Q(owner=self.request.user) | 
            Q(members__user=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class WorkspaceDetailView(RetrieveUpdateDestroyAPIView):
    model = Workspace
    serializer_class = WorkspaceSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "workspace_id"
    
    def get_queryset(self):
        return Workspace.objects.filter(
            Q(owner=self.request.user) | 
            Q(members__user=self.request.user)
        ).distinct()

    def perform_update(self, serializer):
        if not self.request.user==serializer.instance.owner:
            raise PermissionDenied("Only owner can update workspace details")
        serializer.save()

    def perform_destroy(self, instance):
        if not self.request.user==instance.owner:
            raise PermissionDenied("Only owner can delete the workspace")
        instance.delete()

class WorkspaceMemberListCreateView(ListCreateAPIView):
    model = WorkspaceMember
    serializer_class = WorkspaceMemberSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not (workspace.owner==self.request.user or
           workspace.members.filter(user=self.request.user).exists()
           ):
            raise PermissionDenied("Not a member of the workspace")
        return WorkspaceMember.objects.filter(workspace=workspace)

    def perform_create(self, serializer):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not (
            workspace.owner == self.request.user 
            or workspace.members.filter(
                user=self.request.user, role="ADMIN"
            ).exists()
        ):
            raise PermissionDenied("Only the owner or admin can add members")
        serializer.save(workspace=workspace)

class WorkspaceMemberDetailView(RetrieveUpdateDestroyAPIView):
    model = WorkspaceMember
    serializer_class = WorkspaceMemberSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "member_id"

    def get_queryset(self):
        workspace = get_object_or_404(Workspace, id=self.kwargs["workspace_id"])
        if not(
            workspace.owner == self.request.user
            or workspace.members.filter(user=self.request.user).exists()
        ):
            raise PermissionDenied("Not a member of this workspace")
        return WorkspaceMember.objects.filter(workspace=workspace)

    def perform_update(self, serializer):
        workspace = serializer.instance.workspace
        if not (workspace.owner == self.request.user
            or WorkspaceMember.objects.filter(
                workspace=workspace,
                user=self.request.user,
                role="ADMIN"
            ).exists()
        ):
            raise PermissionDenied("Only owner or admin can update members")
        serializer.save()

    def perform_destroy(self, instance):
        if not (instance.workspace.owner == self.request.user
            or WorkspaceMember.objects.filter(
                workspace=instance.workspace,
                user=self.request.user,
                role="ADMIN"
            ).exists()
        ):
            raise PermissionDenied("Only owner or admin can delete members")
        instance.delete()
