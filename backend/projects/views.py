from .models import Project, ProjectMember
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.exceptions import PermissionDenied
from .serializers import ProjectSerializer, ProjectMemberSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsProjectOwner
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

class ProjectMemberListCreateView(ListCreateAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated]
    
    def get_project(self):
        return get_object_or_404(
            Project,
            pk=self.kwargs["pk"]
        )

    def get_queryset(self):
            project = self.get_project()
            return ProjectMember.objects.filter(project=project)

    def perform_create(self, serializer):
        project = self.get_project()

        if project.owner != self.request.user:
            raise PermissionDenied("You are not the owner of this project")

        serializer.save(project=project)

class ProjectMemberDetailView(RetrieveUpdateDestroyAPIView):
    serializer_class = ProjectMemberSerializer
    permission_classes = [IsAuthenticated, IsProjectOwner]
    lookup_url_kwarg = "member_pk"

    def get_queryset(self):
        project_pk = self.kwargs["project_pk"]
        member_pk = self.kwargs["member_pk"]
        return ProjectMember.objects.filter(project_id=project_pk, id=member_pk)
    
    def perform_destroy(self, instance):
        if instance.user == instance.project.owner:
            raise PermissionDenied("You cannot delete an owner")

        instance.delete()