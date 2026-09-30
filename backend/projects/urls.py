from django.urls import path
from .views import (
    ProjectListCreateView,
    ProjectDetailView,
    ProjectMemberListCreateView,
    ProjectMemberDetailView,
    )

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<int:project_id>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<int:project_id>/members/", ProjectMemberListCreateView.as_view(), name="project-member-create"),
    path("<int:project_id>/members/<int:member_id>/", ProjectMemberDetailView.as_view(), name="project-member-detail"),
]
