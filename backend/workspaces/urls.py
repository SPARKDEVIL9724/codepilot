from django.urls import path
from .views import (
    WorkspaceListCreateView,
    WorkspaceDetailView,
    WorkspaceMemberListCreateView,
    WorkspaceMemberDetailView
)

urlpatterns = [
    path("", WorkspaceListCreateView.as_view(), name="workspace-list-create"),
    path("<int:workspace_id>/", WorkspaceDetailView.as_view(), name="workspace-detail"),
    path("<int:workspace_id>/members/", WorkspaceMemberListCreateView.as_view(), name="workspace-member-list-create"),
    path("<int:workspace_id>/members/<int:member_id>/", WorkspaceMemberDetailView.as_view(), name="workspace-member-detail"),
]
