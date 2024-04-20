from rest_framework import serializers
from course.models import Category


class CategorysSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, use_url=True)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']


class CategorySerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'image']
    
    def create(self, validated_data):
        course = Category.objects.create(**validated_data)
        course.save()
        return course
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        if instance.image == None:
            instance.image = self.context.get("image")
        else:
            instance.image = validated_data.get("image", instance.image)
        instance.save()
        return instance
