from rest_framework import serializers

from authen.models import CustomUser
from authen.serializers.serializers import UserInformationSerializer

from chat.models import Conversation, ChatMessage


class MessagesSerializer(serializers.ModelSerializer):
    text = serializers.CharField(required=True)
    # sender_type = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = ['id', "sender", 'text', 'conversation_id', 'timestamp']

    def create(self, validated_data):
        sender = self.context.get('request')
        conversation = self.context.get('conversation')

        create_message = ChatMessage.objects.create(**validated_data)
        create_message.sender = sender
        create_message.conversation_id = conversation
        create_message.save()
        return create_message

    def get_sender_type(self, obj):
        user = self.context.get('request')
        sender = obj.sender
        if sender:
            return 'ini' 
        else:
            return 'res'

    
class ConversationListSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()
    initiator = UserInformationSerializer(read_only=True)
    receiver = UserInformationSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'sender_type']

    def get_sender_type(self, obj):
        user = self.context.get('request')
        if user:
            
            if obj.initiator == user:
                return obj.receiver 
            elif obj.receiver == user:
                return obj.initiator
        return None

    

class MessageListSerializer(serializers.ModelSerializer):
    sender_type = serializers.SerializerMethodField()
    sender = UserInformationSerializer(read_only=True)

    class Meta:
        model = ChatMessage
        fields = ['id', 'sender', 'text', 'timestamp', 'sender_type']
    
    def get_sender_type(self, obj):
        user = self.context['request']
        conversation = obj.conversation
        # print(conversation.initiator_id)
        if user == obj.sender_id:
            if user == conversation.initiator_id:
                return 'initiator'
            elif user == conversation.receiver_id:
                return 'initiator'
        return 'receiver'


class ConversationSerializer(serializers.ModelSerializer):
    messages = MessageListSerializer(many=True, read_only=True)
    sender_type = serializers.SerializerMethodField()
    initiator = UserInformationSerializer(read_only=True)
    receiver = UserInformationSerializer(read_only=True)

    class Meta:
        model = Conversation
        fields = ['id', 'initiator', 'receiver', 'messages', 'sender_type']
    
    def get_sender_type(self, obj):
        user = self.context.get('request')
        print(user)
        if user:
            if obj.initiator == user:
                return obj.receiver 
            elif obj.receiver == user:
                return obj.initiator
        return 'initiator'
