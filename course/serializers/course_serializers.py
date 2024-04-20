from rest_framework import serializers
from course.models import Course, CourseSection, Favorites

from authen.serializers.serializers import UserInformationSerializer
from course.serializers.comment_serializers import CommentsSerializer


class SectionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = CourseSection
        fields = ['id', 'name', 'course']


class CoursesSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    owner = UserInformationSerializer(read_only=True)
    section = SectionsSerializer(many=True, read_only=True)
    comment = CommentsSerializer(many=True, read_only=True)
    favorite = serializers.SerializerMethodField()
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'favorite', 'price', 'discount', 'image', 'category', 'owner', 'section', 'comment']
    
    def get_favorite(self, obj):
        owner = self.context.get("owner")
        user_favorities = Favorites.objects.filter(owner=owner)
        if user_favorities.filter(course__id=obj.id).exists():
            return True
        return False


class CourseSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

    class Meta:
        model = Course
        fields = ['id', 'name', 'price', 'discount', 'image', 'category', 'owner']
    
    def create(self, validated_data):
        course = Course.objects.create(**validated_data)
        course.save()
        return course
    

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.discount = validated_data.get("discount", instance.discount)
        instance.category = validated_data.get("category", instance.category)
        instance.owner = validated_data.get("owner", instance.owner)
        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance