from rest_framework import serializers
from course.models import CourseSection

from course.serializers.course_serializers import CoursesSerializer


class SectionsSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(read_only=True)

    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'course']


class SectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'course']
    
    def create(self, validated_data):
        course = CourseSection.objects.create(**validated_data)
        course.save()
        return course
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.course = validated_data.get("course", instance.course)
        instance.save()
        return instance