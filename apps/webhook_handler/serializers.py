from rest_framework import serializers
from .models import Conversation, Message

class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Message.
    
    Converte mensagens para JSON, incluindo campos essenciais como
    id, direção, conteúdo e timestamp.
    """
    class Meta:
        model = Message
        fields = ['id', 'direction', 'content', 'timestamp']

class ConversationSerializer(serializers.ModelSerializer):
    """
    Serializer para o modelo Conversation.
    
    Converte conversas para JSON, incluindo todas as mensagens relacionadas
    através de um relacionamento aninhado.
    """
    messages = MessageSerializer(many=True, read_only=True)
    
    class Meta:
        model = Conversation
        fields = ['id', 'state', 'messages']


class WebhookSerializer(serializers.Serializer):
    """
    Serializer para validar os dados recebidos via webhook.
    
    Valida o tipo de evento, timestamp e dados específicos do evento
    antes do processamento.
    """
    type = serializers.ChoiceField(
        choices=[
            'NEW_CONVERSATION',
            'NEW_MESSAGE',
            'CLOSE_CONVERSATION'
        ]
    )
    timestamp = serializers.DateTimeField()
    data = serializers.DictField()
