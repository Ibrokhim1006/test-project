from django.db import models
from authen.models import CustomUser


class Conversation(models.Model):
    initiator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='initiated_conversations')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True, related_name='received_conversations')
    start_time = models.DateTimeField(auto_now_add=True, verbose_name='Time stamp', null=True, blank=True)

    class Meta:
        db_table = "table_conversation"
        verbose_name = "Conversation"
        verbose_name_plural = "Conversations"


class ChatMessage(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    text = models.CharField(max_length=200, blank=True, verbose_name='Text')
    attachment = models.FileField(blank=True, null=True, verbose_name='File Uploaded')
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, verbose_name='Conversation Identity',related_name='messages', null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Time stamp', null=True, blank=True)
