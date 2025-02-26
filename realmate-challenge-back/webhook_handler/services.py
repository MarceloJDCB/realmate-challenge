from django.shortcuts import get_object_or_404
from .models import Conversation, Message

class WebhookService:
    """
    Serviço responsável por processar eventos de webhook e gerenciar conversas e mensagens.
    
    Esta classe separa a regra de negócio da camada de visualização para facilitar testes unitários
    e manter a responsabilidade única dos componentes.
    """
    
    @staticmethod
    def create_conversation(data: dict) -> Conversation:
        """
        Cria uma nova conversa no sistema.

        Args:
            data (dict): Dicionário contendo os dados da conversa, incluindo o ID.

        Returns:
            Conversation: A nova conversa criada.
        """
        return Conversation.objects.create(id=data['data']['id'])
    
    @staticmethod
    def create_message(data: dict) -> Message:
        """
        Cria uma nova mensagem em uma conversa existente.

        Args:
            data (dict): Dicionário contendo os dados da mensagem, incluindo ID da conversa,
                        direção, conteúdo e timestamp.

        Returns:
            Message: A nova mensagem criada.

        Raises:
            ValueError: Se tentar adicionar mensagem a uma conversa fechada.
            Http404: Se a conversa não for encontrada.
        """
        conversation = get_object_or_404(Conversation, id=data['data']['conversation_id'])
        if conversation.state == Conversation.CLOSED_CHOICE:
            raise ValueError('Cannot add message to closed conversation')
            
        return Message.objects.create(
            id=data['data']['id'],
            conversation=conversation,
            direction=data['data']['direction'],
            content=data['data']['content'],
            timestamp=data['timestamp']
        )
    
    @staticmethod
    def close_conversation(data: dict) -> Conversation:
        """
        Fecha uma conversa existente.

        Args:
            data (dict): Dicionário contendo o ID da conversa a ser fechada.

        Returns:
            Conversation: A conversa atualizada.

        Raises:
            Http404: Se a conversa não for encontrada.
        """
        conversation = get_object_or_404(Conversation, id=data['data']['id'])
        conversation.state = Conversation.CLOSED_CHOICE
        conversation.save()
        return conversation
