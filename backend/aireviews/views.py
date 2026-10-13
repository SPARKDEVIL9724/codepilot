from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import AIReview
from .serializers import AIReviewSerializer
from .services import review_code, AIReviewError
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied, APIException
from django.shortcuts import get_object_or_404
from workspaces.models import Workspace
from projects.models import Project
from codesnippets.models import CodeSnippet

class AIReviewUnavailable(APIException):
    status_code = 503
    default_detail = "AI review is temporarily unavailable"
    default_code = "ai_review_unavailable"

class AIReviewView(APIView):
    permission_classes = [IsAuthenticated]

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
                pk=request.user.pk
            ).exists()
        ):
            raise PermissionDenied("User is not a project owner or member")

        try:
            review = review_code(snippet.content)
        except AIReviewError as exc:
            raise AIReviewUnavailable() from exc
        
        review_obj, _ = AIReview.objects.update_or_create(
            snippet=snippet,
            defaults={
                "summary": review["summary"],
                "findings": review["findings"],
            }
        )

        serializer = AIReviewSerializer(review_obj)
        return Response(serializer.data, status=status.HTTP_200_OK)