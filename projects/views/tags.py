from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from projects.models import Tag
from projects.serializers import TagListSerializer, TagSerializer
from rest_framework import status


class TagListCreateAPIView(APIView):
    def get(self, request: Request) -> Response:
        all_tags = Tag.objects.all()
        list_tags = TagListSerializer(all_tags, many=True)
        return Response(list_tags.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        create_tag = TagListSerializer(data=request.data)
        if create_tag.is_valid():
            create_tag.save()
            return Response(create_tag.data, status=status.HTTP_201_CREATED)
        return Response(create_tag.errors, status=status.HTTP_400_BAD_REQUEST)


class TagDetailAPIView(APIView):
    def get_object(self) -> Tag:
        pk = self.kwargs['pk']
        try:
            obj = Tag.objects.get(pk=pk)
        except Tag.DoesNotExist:
            raise NotFound(f'Tag with {pk} ID not found')
        return obj

    def get(self, request: Request, *args, **kwargs) -> Response:
        tag = self.get_object()

        serializer = TagSerializer(tag)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    def put(self, request: Request, *args, **kwargs) -> Response:
        tag = self.get_object()

        serializer = TagSerializer(tag, data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

            return Response(
                serializer.validated_data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request: Request, *args, **kwargs) -> Response:
        tag = self.get_object()
        tag.delete()

        return Response(
            data={"message": "Tag was deleted successfully"},
            status=status.HTTP_200_OK
        )
