from drf_yasg.utils import swagger_auto_schema

from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAuth
from utils.response import success_response, success_created_response, bad_request_response

from course.models import CommentCourse, Grade
from course.serializers.comment_serializers import CommentsSerializer, CommentSerializer, GradeSerializer


class GradeView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request):
        queryset = Grade.objects.all().order_by('id')
        serializer = GradeSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)


class CommentsView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request):
        serializers = CommentSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class CommentView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    @swagger_auto_schema(request_body=CommentSerializer)
    def put(self, request, pk):
        serializers = CommentSerializer(instance=CommentCourse.objects.filter(id=pk)[0], context={"request": request}, data=request.data, partial=True,)
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_response(serializers.data)
        return bad_request_response(serializers.errors)

    def delete(self, request, pk):
        objects_get = CommentCourse.objects.get(id=pk)
        objects_get.delete()
        return success_response("delete success")


class CommentCourseView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]
    filter_backends = [DjangoFilterBackend]
    serializer_class = CommentsSerializer
    filterset_fields = ["grade"]

    def get(self, request, pk):
        queryset = CommentCourse.objects.filter(course=pk).order_by('-create_at')
        grade = request.query_params.get("grade", None)
        if grade:
            queryset = queryset.filter(Q(grade=grade))
        serializer = self.serializer_class(queryset, many=True)
        return success_response(serializer.data)