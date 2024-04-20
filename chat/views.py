from django.shortcuts import get_object_or_404
from django.db.models import Q

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework_simplejwt.authentication import JWTAuthentication

from utils.renderers import UserRenderers
from utils.permissons import IsAuth
from utils.response import success_response, success_created_response, bad_request_response

from authen.models import CustomUser
from authen.serializers.serializers import UserInformationSerializer

from chat.models import Conversation, ChatMessage
from chat.serializers import (
    ConversationListSerializer,
    ConversationSerializer,
    MessagesSerializer,
    MessageListSerializer
)






class StartConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]
    filter_backends = [DjangoFilterBackend]
    serializer_class = UserInformationSerializer
    filterset_fields = ["username"]

    def get(self, request):
        queryset = CustomUser.objects.all()
        search_username = request.query_params.get("username", None)

        if search_username:
            queryset = queryset.filter(Q(username__icontains=search_username))
        serializer = UserInformationSerializer(queryset, many=True)
        return success_response(serializer.data)


    def post(self, request):
        data = request.data

        username = data['username']
        try:
            participant = CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Вы не можете общаться с пользователем, которого не существует.'})
        conversation = Conversation.objects.filter(Q(initiator=request.user, receiver=participant) |
                                                   Q(initiator=participant, receiver=request.user))
        if conversation.exists():
            return Response({"message": "Разговор уже существует"}, status=status.HTTP_200_OK)
        else:
            conversation = Conversation.objects.create(initiator=request.user, receiver=participant)
            return Response(ConversationSerializer(instance=conversation).data, status=status.HTTP_200_OK)


class GetConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]
    filterset_fields = ["text"]

    def get(self, request, convo_id):
        text = request.query_params.get("text", None)
        if text:
            conversation = ChatMessage.objects.select_related('conversation_id').filter(
                Q(conversation_id=convo_id), Q(text__icontains=text)
            )
            page = self.paginate_queryset(conversation)
            serializer = MessageListSerializer(conversation, many=True, context={'request': request})

            return Response(serializer.data, status=status.HTTP_200_OK)

        conversation = get_object_or_404(Conversation, id=convo_id)
        messages = conversation.message_set.all()  # Retrieve all messages for the conversation
        # page = self.paginate_queryset(messages)
        serializer = ConversationSerializer(conversation, context={'request': request.user})
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]
    filterset_fields = ["text"]

    def get(self, request, convo_id):
        conversation = get_object_or_404(Conversation, id=convo_id)

        messages = conversation.messages.all()  # Retrieve all messages for the conversation
        # page = self.paginate_queryset(messages)

        serializer = ConversationSerializer(conversation, context={'request': request.user.id})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, convo_id):
        conversation = get_object_or_404(Conversation, id=convo_id)
        serializer = MessagesSerializer(data=request.data, context={
            "request": request.user,
            "conversation": conversation
        })
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConversationView(APIView):
    render_classes = [UserRenderers]
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuth]

    def get(self, request):

        conversation_list = Conversation.objects.filter(Q(initiator=request.user.id) |
                                                        Q(receiver=request.user.id))
        serializer = ConversationListSerializer(instance=conversation_list, many=True, context={"request": request.user.id})
        # serializer = super().page(conversation_list, ConversationListSerializer, request)

        return Response(serializer.data, status=status.HTTP_200_OK)
