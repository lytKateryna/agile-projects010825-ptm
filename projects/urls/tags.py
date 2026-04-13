from django.urls import path

from projects.views.tags import TagListCreateAPIView, TagDetailAPIView


urlpatterns = [
    path('', TagListCreateAPIView.as_view()),
    path('<int:pk>/', TagDetailAPIView.as_view()),
]
