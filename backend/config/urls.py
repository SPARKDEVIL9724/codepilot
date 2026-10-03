from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/' ,include('users.urls')),
    path('api/workspaces/' ,include('workspaces.urls')),
    path('api/workspaces/<int:workspace_id>/projects/' ,include('projects.urls')),
    path('api/workspaces/<int:workspace_id>/projects/<int:project_id>/documents/' ,include('documents.urls')),
    path('api/workspaces/<int:workspace_id>/projects/<int:project_id>/codesnippets/' ,include('codesnippets.urls')),
]