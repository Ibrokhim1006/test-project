from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAdmin, IsAuth
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response

from course.models import Category, Course
from course.serializers.category_serializers import CategorysSerializer, CategorySerializer
from course.serializers.course_serializers import CoursesSerializer


class CategorysView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Category.objects.all().order_by('-create_at')
        serializer = CategorysSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def post(self, request):
        valid_fields = {'id', 'name', 'image',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = CategorySerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CategroyView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        objects_list = get_object_or_404(Category, id=pk)
        serializers = CategorysSerializer(objects_list)
        return success_response(serializers.data)

    @swagger_auto_schema(request_body=CategorySerializer)
    def put(self, request, pk):
        valid_fields = {'name', 'image',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = CategorySerializer(instance=Category.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    def delete(self, request, pk):
        objects_get = Category.objects.get(id=pk)
        objects_get.delete()
        return success_response("delete success")


class CategoryCourseView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request, pk):
        queryset = Course.objects.filter(category=pk).order_by('-create_at')
        serializer = CoursesSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)