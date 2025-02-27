import logging
from .models import Conversation, Message

logger = logging.getLogger('webhook_handler')

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
        conversation_id = data['data']['id']
        logger.info(f"Creating new conversation with ID: {conversation_id}")
        conversation = Conversation.objects.create(id=conversation_id)
        logger.debug(f"Conversation {conversation_id} created successfully")
        return conversation
    
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
            ValueError: Se tentar adicionar mensagem a uma conversa fechada ou se a conversa não existir.
        """
        conversation_id = data['data']['conversation_id']
        message_id = data['data']['id']
        logger.info(f"Creating new message {message_id} for conversation {conversation_id}")
        
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            logger.debug(f"Found conversation {conversation_id}")
        except Conversation.DoesNotExist:
            logger.error(f"Conversation {conversation_id} not found")
            raise ValueError('Conversation not found')
            
        if conversation.state == Conversation.CLOSED_CHOICE:
            logger.error(f"Attempted to add message to closed conversation {conversation_id}")
            raise ValueError('Cannot add message to closed conversation')
            
        message = Message.objects.create(
            id=message_id,
            conversation=conversation,
            direction=data['data']['direction'],
            content=data['data']['content'],
            timestamp=data['timestamp']
        )
        logger.info(f"Message {message_id} created successfully in conversation {conversation_id}")
        return message
    
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
        conversation_id = data['data']['id']
        logger.info(f"Closing conversation {conversation_id}")
        try:
            conversation = Conversation.objects.get(id=conversation_id)
            logger.debug(f"Found conversation {conversation_id}")
        except Conversation.DoesNotExist:
            logger.error(f"Conversation {conversation_id} not found")
            raise ValueError('Conversation not found')
        conversation.state = Conversation.CLOSED_CHOICE
        conversation.save()
        
        logger.info(f"Conversation {conversation_id} closed successfully")
        return conversation
