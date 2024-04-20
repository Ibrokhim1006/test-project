from rest_framework import serializers
from course.models import Lesson

from course.serializers.section_serializers import SectionsSerializer


class LessonsSerializer(serializers.ModelSerializer):
    video = serializers.FileField(max_length=None, use_url=True)
    section = SectionsSerializer(read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'content', 'video', 'section']


class LessonSerializer(serializers.ModelSerializer):
    video = serializers.FileField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

    class Meta:
        model = Lesson
        fields = ['id', 'name', 'content', 'video', 'section']
    
    def create(self, validated_data):
        course = Lesson.objects.create(**validated_data)
        course.save()
        return course
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.content = validated_data.get("content", instance.content)
        instance.section = validated_data.get("section", instance.section)
        instance.save()
        return instance