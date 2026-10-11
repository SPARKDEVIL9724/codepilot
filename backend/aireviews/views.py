from rest_framework.views import APIView
from .models import AIReview
from .serializers import AIReviewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace
from projects.models import Project
from codesnippets.models import CodeSnippet

class AIReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AIReviewSerializer

    def review_code(code):
        pass

    def post(self, request, workspace_id, project_id, snippet_id):
        project = get_object_or_404(
            Project,
            id=project_id,
            workspace=get_object_or_404(
                Workspace,
                id=workspace_id
            )
        )
        snippet = get_object_or_404(
            CodeSnippet,
            id=snippet_id,
            project=project
        )

        if not (
            request.user == project.owner
            or project.members.filter(
                user=request.user
            ).exists()
        ):
            raise PermissionDenied("User is not a project owner or member")

        review, created = AIR32