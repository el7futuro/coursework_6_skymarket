from functools import partial
from rest_framework import pagination, viewsets
from rest_framework.decorators import action
from ads.models import Ad, Comment
from ads.serializers import AdSerializer, AdDetailSerializer, CommentSerializer
from rest_framework.views import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from ads.permissions import UserPermission
from users.models import User


class AdPagination(pagination.PageNumberPagination):
    page_size = 5


class CommentPagination(pagination.PageNumberPagination):
    page_size = 5


class AdViewSet(viewsets.ModelViewSet):
    queryset = Ad.objects.all()
    pagination_class = AdPagination
    permission_classes = [UserPermission]

    def list(self, request, *args, **kwargs):
        queryset = Ad.objects.all()
        serializer = AdSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.id == request.data['author']:
            serializer = AdSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Ad.objects.all()

        user = get_object_or_404(queryset, pk=pk)
        serializer = AdDetailSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = Ad.objects.all()

        user = get_object_or_404(queryset, pk=pk)

        serializer = AdSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = Ad.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(methods=['get'], detail=True)
    def me(self, request, pk=None):
        queryset = Ad.objects.get(pk=User.objects.get(pk))
        serializer = AdSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    pagination_class = CommentPagination
    permission_classes = [UserPermission]

    def list(self, request, *args, **kwargs):
        queryset = Comment.objects.all()
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        if request.user.id == request.data['author']:
            serializer = CommentSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response("Unauthorized", status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        queryset = Comment.objects.all()

        user = get_object_or_404(queryset, pk=pk)
        serializer = CommentSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        queryset = Comment.objects.all()

        user = get_object_or_404(queryset, pk=pk)

        serializer = CommentSerializer(user, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def partial_update(self, request, pk=None, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)

    def destroy(self, request, pk=None, *args, **kwargs):
        queryset = Comment.objects.all()
        user = get_object_or_404(queryset, pk=pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
