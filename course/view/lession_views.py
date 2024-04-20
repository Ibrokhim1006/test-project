from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAdmin, IsAuth
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response

from course.models import Lesson
from course.serializers.lesson_serializers import LessonsSerializer, LessonSerializer


class LessonsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Lesson.objects.all().order_by('-create_at')
        serializer = LessonsSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=LessonSerializer)
    def post(self, request):
        valid_fields = {'id', 'name', 'content', 'video', 'section',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = LessonSerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class LessonView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        objects_list = get_object_or_404(Lesson, id=pk)
        serializers = LessonsSerializer(objects_list)
        return success_response(serializers.data)

    @swagger_auto_schema(request_body=LessonSerializer)
    def put(self, request, pk):
        valid_fields = {'id', 'name', 'content', 'video', 'section',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = LessonSerializer(instance=Lesson.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    def delete(self, request, pk):
        objects_get = Lesson.objects.get(id=pk)
        objects_get.delete()
        return success_response("delete success")


class LessonSectionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request, pk):
        queryset = Lesson.objects.filter(section=pk).order_by('-create_at')
        serializer = LessonsSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)
