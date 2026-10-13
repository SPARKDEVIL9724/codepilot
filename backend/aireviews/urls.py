from django.urls import path
from .views import AIReviewView


urlpatterns = [
    path("",AIReviewView.as_view(), name="ai-review")
]
