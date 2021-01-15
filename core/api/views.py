from django.http import Http404
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet

from core.models import User, Organization, WorkPlace, Post, Person, WorkTime
from core.api.filters import WorkPlaceFilter, PostFilter, PersonFilter, WorkTimeFilter
from core.api.serializers import UserSerializer, OrganizationSerializer, WorkPlaceSerializer, PostSerializer,\
    PersonSerializer, WorkTimeSerializer


class UserViewSet(GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = None

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)

    def get_object(self):
        return self.request.user

    @action(methods=['get'], detail=False)
    def me(self, *args, **kwargs):
        try:
            instance = self.get_object()
        except User.DoesNotExist:
            raise Http404
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(methods=['patch'], detail=False)
    def edit(self, request, *args, **kwargs):
        instance = self.request.user
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrganizationViewSet(ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class WorkPlaceViewSet(ModelViewSet):
    filter_class = WorkPlaceFilter
    queryset = WorkPlace.objects.all()
    serializer_class = WorkPlaceSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user)


class PostViewSet(ModelViewSet):
    filter_class = PostFilter
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user)


class PersonViewSet(ModelViewSet):
    filter_class = PersonFilter
    queryset = Person.objects.all()
    serializer_class = PersonSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user)


class WorkTimeViewSet(ModelViewSet):
    filter_class = WorkTimeFilter
    queryset = WorkTime.objects.all()
    serializer_class = WorkTimeSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        return super().get_queryset().filter(organization__owner=self.request.user)
