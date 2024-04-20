from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAuth
from utils.response import success_response, success_created_response, bad_request_response

from course.models import Favorites
from course.serializers.favorite_serializers import FavoritesSerializer, FavoriteSerializer


class FavoritesView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request):
        queryset = Favorites.objects.filter(owner=request.user).order_by('id')
        serializer = FavoritesSerializer(queryset, many=True, context={'request': request})
        return success_response(serializer.data)

    @swagger_auto_schema(request_body=FavoriteSerializer)
    def post(self, request):
        serializers = FavoriteSerializer(data=request.data, context={'request': request, 'owner': request.user})
        if serializers.is_valid(raise_exception=True):
            serializers.save()
            return success_created_response(serializers.data)
        return bad_request_response(serializers.errors)


class FavoriteViews(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def delete(self, request, pk):
        objects_get = Favorites.objects.get(course=pk)
        objects_get.delete()
        return success_response("delete success")
