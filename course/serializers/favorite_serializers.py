from rest_framework import serializers
from course.models import Favorites
from course.serializers.course_serializers import CoursesSerializer


class FavoritesSerializer(serializers.ModelSerializer):
    course = CoursesSerializer(read_only=True)

    class Meta:
        model = Favorites
        fields = ["id", "course", "owner", "is_active", "create_at"]


class FavoriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favorites
        fields = ["id", "course", "owner", "is_active", "create_at"]

    def create(self, validated_data):
        owner = self.context.get("owner")
        favorite = Favorites.objects.create(**validated_data)
        favorite.owner = owner
        favorite.save()
        return favorite
