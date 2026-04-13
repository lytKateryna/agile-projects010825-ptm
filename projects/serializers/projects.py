from rest_framework import serializers

from projects.models import Project


class ProjectListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "created_at"
        ]


class CreateProjectSerializer(serializers.ModelSerializer):
   created_at = serializers.DateField(read_only=True)

   class Meta:
       model = Project
       fields = ('name', 'description', 'created_at')

   def validate_description(self, value: str) -> str:
       if len(value) < 30:
           raise serializers.ValidationError(
               "Description must be at least 30 characters long"
           )

       return value


class ProjectDetailSerializer(serializers.ModelSerializer):

   class Meta:
       model = Project
       fields = ('id', 'name', 'description', 'count_of_files')
