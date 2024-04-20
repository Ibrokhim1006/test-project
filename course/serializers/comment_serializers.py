from rest_framework import serializers
from course.models import CommentCourse, Grade
from authen.serializers.serializers import UserInformationSerializer


class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ['id', 'name']


class CommentsSerializer(serializers.ModelSerializer):
    grade = GradeSerializer(read_only=True)
    owner = UserInformationSerializer(read_only=True)
    
    class Meta:
        model = CommentCourse
        fields = ['id', 'comment', 'course', 'owner', 'grade', 'create_at']


class CommentSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CommentCourse
        fields = ['id', 'comment', 'course', 'owner', 'grade', 'create_at']

    def create(self, validated_data):
        owner = self.context.get('owner')
        course = CommentCourse.objects.create(**validated_data)
        course.owner = owner
        course.save()
        return course

