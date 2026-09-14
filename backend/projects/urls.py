from django.urls import path
from .views import ProjectListCreateView, ProjectDetailView, ProjectMemberListCreateView, ProjectMemberDetailView

urlpatterns = [
    path("", ProjectListCreateView.as_view(), name="project-list-create"),
    path("<int:pk>/", ProjectDetailView.as_view(), name="project-detail"),
    path("<int:pk>/members/", ProjectMemberListCreateView.as_view(), name="project-member-create"),
    path("<int:project_pk>/members/<int:member_pk>/", ProjectMemberDetailView.as_view(), name="project-member-detail"),
]
