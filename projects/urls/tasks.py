from django.urls import path

from projects.views.tasks import TaskListCreateAPIView, TaskRetrieveUpdateDestroyAPIView


urlpatterns = [
    path('', TaskListCreateAPIView.as_view()),
    path('<int:pk>/', TaskRetrieveUpdateDestroyAPIView.as_view()),
]
