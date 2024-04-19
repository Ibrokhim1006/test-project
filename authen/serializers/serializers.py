from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from authen.models import CustomUser


class UserSignUpSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=20, min_length=1, required=True, validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "password", "confirm_password"]
        extra_kwargs = {"first_name": {"required": True}, "last_name": {"required": True}}

    def validate_password(self, value):
        try:
            validate_password(value)
        except ValidationError as exc:
            raise serializers.ValidationError(str(exc))
        return value

    def create(self, validated_data):
        password = validated_data.get("password")
        confirm_password = validated_data.pop("confirm_password")
        if password != confirm_password:
            raise serializers.ValidationError({"error": "Those passwords don't match"})
        user = CustomUser.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    avatar = serializers.ImageField(max_length=None, allow_empty_file=False, allow_null=False, use_url=False, required=False,)

    class Meta:
        model = CustomUser
        fields = ["id", "first_name", "last_name", "avatar",]

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get("first_name", instance.first_name)
        instance.last_name = validated_data.get("last_name", instance.last_name)
        if instance.avatar == None:
            instance.avatar = self.context.get("avatar")
        else:
            instance.avatar = validated_data.get("avatar", instance.avatar)
        instance.save()
        return instance

class UserSignInSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = CustomUser
        fields = ["username", "password"]
        read_only_fields = ("username",)

    def validate(self, data):
        if self.context.get("request") and self.context["request"].method == "POST":
            allowed_keys = set(self.fields.keys())
            input_keys = set(data.keys())
            extra_keys = input_keys - allowed_keys
            if extra_keys:
                raise serializers.ValidationError(f"Additional keys are not allowed: {', '.join(extra_keys)}")
        return data


class UserInformationSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(max_length=None, use_url=True)

    class Meta:
        model = CustomUser
        fields = ["id", "username", "first_name", "last_name", "avatar"]
