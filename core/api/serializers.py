from rest_framework import serializers

from core.models import User, Organization, WorkPlace, Post, Person, WorkTime


class UserSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    token = serializers.SerializerMethodField(source='get_token')

    class Meta:
        model = User
        fields = ('id', 'email', 'name', 'token')
        read_only_fields = ['email', 'id']

    def get_token(self, user):
        token = user.auth_tokens.first()
        if token:
            return token.key


class OrganizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Organization
        fields = '__all__'


class WorkPlaceSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkPlace
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PersonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Person
        fields = '__all__'


class WorkTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkTime
        fields = '__all__'
