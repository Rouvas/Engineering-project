from django_filters import rest_framework as filters

from core.models import WorkPlace, Post, Person, WorkTime


class WorkPlaceFilter(filters.FilterSet):
    class Meta:
        model = WorkPlace
        fields = ('id', 'organization',)


class PostFilter(filters.FilterSet):

    class Meta:
        model = Post
        fields = ('id', 'organization', 'work_place')


class PersonFilter(filters.FilterSet):

    class Meta:
        model = Person
        fields = ('id', 'organization', 'work_place', 'post', 'status')


class WorkTimeFilter(filters.FilterSet):

    class Meta:
        model = WorkTime
        fields = ('id', 'person')
