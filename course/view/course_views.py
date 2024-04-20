from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAdmin
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response, user_not_found_response

from django.core.exceptions import ObjectDoesNotExist

from course.models import Course
from course.serializers.course_serializers import CoursesSerializer, CourseSerializer


class CoursesView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = Course.objects.all().order_by('-create_at')
        serializer = CoursesSerializer(queryset, many=True, context={'request': request, 'owner': request.user})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        valid_fields = {'id', 'name', 'price', 'discount', 'image', 'category', 'owner',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = CourseSerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CourseView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        objects_list = get_object_or_404(Course, id=pk)
        serializers = CoursesSerializer(objects_list, context={'request': request, 'owner': request.user})
        return success_response(serializers.data)

    @swagger_auto_schema(request_body=CourseSerializer)
    def put(self, request, pk):
        valid_fields = {'id', 'name', 'price', 'discount', 'image', 'category', 'owner',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = CourseSerializer(instance=Course.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(id=pk)
            if course.delete_if_no_course_section():
                return success_response({"message": "Course deleted successfully."})
            else:
                return bad_request_response({"message": "There are courses linked to a section that cannot be deleted."})
        except ObjectDoesNotExist:
            return user_not_found_response({"message": "No such Course exists."})