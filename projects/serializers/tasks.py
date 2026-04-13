from rest_framework import serializers

from projects.models import Task


class TaskListSerializer(serializers.ModelSerializer):
   class Meta:
       model = Task
       fields = ['id', 'name', 'status', 'priority']


class TaskCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'priority',
            'project',
            'due_date',
            'assignee',
            'created_by',
        )


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'priority',
            'project',
            'created_at',
            'due_date',
            'tags',
            'assignee',
            'created_by',
        )


class TaskUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = (
            'name',
            'description',
            'status',
            'priority',
            'project',
            'created_at',
            'due_date',
            'tags',
            'assignee',
            'created_by',
        )
