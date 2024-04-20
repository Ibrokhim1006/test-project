from django.urls import path

from chat.views import (
    StartConversationView,
    ConversationView,
    GetConversationView,
)

urlpatterns = [
    # create room
    path('chat/create_room/', StartConversationView.as_view(), name='start_convo'),
    # get room on initiator and receiver
    path('chat/rooms/', ConversationView.as_view(), name='conversations'),
    # get conversation  all messages
    path('chat/conversation/<int:convo_id>/', GetConversationView.as_view(), name='get_conversation'),

]
