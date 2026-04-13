from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.exceptions import NotFound
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend

from projects.models import Task
from projects.serializers import (
    TaskListSerializer,
    TaskCreateSerializer,
    TaskDetailSerializer,
    TaskUpdateSerializer
)


class TaskViewSet(ModelViewSet):

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    # filterset_fields = ['status', 'priority', 'project', 'assignee', 'due_date']
    filterset_fields = ['status', 'priority', 'project', 'assignee']
    search_fields = ['name']
    # ordering_fields = ['due_date']

    def get_queryset(self):
        queryset = Task.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskListSerializer
        elif self.action in ['update', 'partial_update']:
            return TaskUpdateSerializer
        elif self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskCreateSerializer


class TaskListCreateAPIView(APIView):
    def get_queryset(self):
        queryset = Task.objects.all()

        return queryset

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskListSerializer
        return TaskCreateSerializer

    def get(self, request: Request, *args, **kwargs) -> Response:
        qs = self.get_queryset()

        serializer = self.get_serializer_class()

        serializer = serializer(qs, many=True)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer_class()

        serializer = serializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                data=serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            data=serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class TaskRetrieveUpdateDestroyAPIView(APIView):
    def get_serializer_class(self):
        if self.request.method == 'GET':
            return TaskDetailSerializer
        return TaskUpdateSerializer

    def get_object(self) -> Task:
        pk = self.kwargs['pk']

        try:
            obj = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            raise NotFound(f'Task with {pk} ID does not exist')
        return obj

    def update(self, partial: bool = False):
        obj = self.get_object()

        serializer = self.get_serializer_class()

        serializer = serializer(instance=obj, data=self.request.data, partial=partial)

        if serializer.is_valid():
            serializer.save()

            return serializer.data, status.HTTP_200_OK

        return serializer.errors, status.HTTP_400_BAD_REQUEST

    def get(self, request: Request, *args, **kwargs) -> Response:
        task = self.get_object()

        serializer = self.get_serializer_class()

        serializer = serializer(task)

        return Response(
            data=serializer.data,
            status=status.HTTP_200_OK
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        instance, status_code = self.update()

        return Response(
            data=instance,
            status=status_code
        )

    def patch(self, request: Request, *args, **kwargs) -> Response:
        instance, status_code = self.update(partial=True)

        return Response(
            data=instance,
            status=status_code
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        task = self.get_object()

        task.delete()

        return Response(
            data={},
            status=status.HTTP_204_NO_CONTENT
        )


@api_view(['GET',])
def get_all_tasks(request: Request) -> Response:
    all_tasks = Task.objects.all()

    if not all_tasks.exists():
        return Response(
            data=[],
            status=status.HTTP_200_OK,
        )

    serialized_data = TaskListSerializer(all_tasks, many=True)

    return Response(
        data=serialized_data.data,
        status=status.HTTP_200_OK
    )
