from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from webhook_handler.tasks import process_webhook
from .models import Conversation
from .serializers import ConversationSerializer, WebhookSerializer
from .mixins import WebhookAuthentication


class WebhookViewSet(viewsets.ViewSet):
    """
    ViewSet para manipulação de webhooks e monitoramento de tarefas assíncronas.

    Fornece endpoints para:
    - Receber webhooks e processar de forma assíncrona
    - Verificar o status de tarefas em processamento
    """
    authentication_classes = [WebhookAuthentication]
    
    @action(detail=False, methods=['post'])
    def webhook(self, request):
        """
        Recebe dados do webhook e inicia processamento assíncrono.
        
        Returns:
            Response com ID da tarefa criada e status 202 (Accepted)
        """
        serializer = WebhookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        task_id = process_webhook.delay(serializer.validated_data)
        return Response({'task_id': task_id}, status=status.HTTP_202_ACCEPTED)

    @action(detail=True, methods=['get'])
    def task_status(self, request, pk=None):
        """
        Verifica o status de uma tarefa específica.
        
        Args:
            pk: ID da tarefa a ser verificada
            
        Returns:
            Response com o status atual da tarefa
        """
        task = process_webhook.AsyncResult(pk)
        return Response({'status': task.status})


class ConversationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet somente leitura para listar e recuperar conversas.
    
    Fornece endpoints para listar todas as conversas e recuperar
    conversas específicas por ID, incluindo suas mensagens.
    """
    queryset = Conversation.objects.prefetch_related('messages').all()
    serializer_class = ConversationSerializer

