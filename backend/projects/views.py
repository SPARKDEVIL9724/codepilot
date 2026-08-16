from .models import Project, ProjectMember
from rest_framework.generics import CreateAPIView,ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner
from django.shortcuts import get_object_or_404

class ProjectListCreateView(ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class ProjectDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Project.objects.all()

class ProjectMemberCreateView(CreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_project(self):
        return get_object_or_404(
            Project,
            pk=self.kwargs["pk"]
        )

    def perform_create(self, serializer):
        project = self.get_project()

        if project.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this project")

        serializer.svae(project=project)
    