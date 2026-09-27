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