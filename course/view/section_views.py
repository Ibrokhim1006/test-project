from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema

from django.core.exceptions import ObjectDoesNotExist

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAdmin, IsAuth
from utils.expected_fields import check_required_key
from utils.response import success_response, success_created_response, bad_request_response, user_not_found_response

from course.models import CourseSection
from course.serializers.section_serializers import SectionsSerializer, SectionSerializer


class SectionsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request):
        queryset = CourseSection.objects.all().order_by('-create_at')
        serializer = SectionsSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=SectionSerializer)
    def post(self, request):
        valid_fields = {'id', 'name', 'course',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = SectionSerializer(data=request.data, context={'request': request})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class SectionView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        objects_list = get_object_or_404(CourseSection, id=pk)
        serializers = SectionsSerializer(objects_list)
        return success_response(serializers.data)

    @swagger_auto_schema(request_body=SectionSerializer)
    def put(self, request, pk):
        valid_fields = {'id', 'name', 'course',}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")
        serializers = SectionSerializer(instance=CourseSection.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    def delete(self, request, pk):
        try:
            course = CourseSection.objects.get(id=pk)
            if course.delete_if_no_lesson():
                return success_response({"message": "Section deleted successfully."})
            else:
                return bad_request_response({"message": "There are courses linked to a Lesson that cannot be deleted."})
        except ObjectDoesNotExist:
            return user_not_found_response({"message": "No such Section exists."})


class SectionCourseView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request, pk):
        queryset = CourseSection.objects.filter(course=pk).order_by('-create_at')
        serializer = SectionsSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)
